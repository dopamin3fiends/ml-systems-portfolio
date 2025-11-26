"""
Web Automation Framework - Browser Automation Engine
Selenium-based browser automation with action execution
"""

import time
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.edge.options import Options as EdgeOptions
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    webdriver = None

try:
    from models import (
        BrowserConfig, BrowserAction, Workflow, SessionResult,
        BrowserType, ActionType, SessionStatus
    )
except ImportError:
    from .models import (
        BrowserConfig, BrowserAction, Workflow, SessionResult,
        BrowserType, ActionType, SessionStatus
    )


class AutomationEngine:
    """
    Browser automation engine using Selenium
    
    Features:
    - Multi-browser support (Chrome, Firefox, Edge)
    - Headless mode for background execution
    - Proxy configuration
    - Custom user agents
    - Screenshot capture
    - JavaScript execution
    - Data extraction
    """
    
    def __init__(self, output_dir: str = "data/tmp/automation_output"):
        """
        Initialize automation engine
        
        Args:
            output_dir: Directory for screenshots and output files
        """
        if not SELENIUM_AVAILABLE:
            raise ImportError("selenium library required. Install with: pip install selenium")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.driver = None
    
    def _create_driver(self, config: BrowserConfig):
        """
        Create browser driver with configuration
        
        Args:
            config: Browser configuration
        """
        if config.browser_type == BrowserType.CHROME:
            options = ChromeOptions()
            
            if config.headless:
                options.add_argument("--headless")
            
            if config.user_agent:
                options.add_argument(f"user-agent={config.user_agent}")
            
            if config.proxy:
                options.add_argument(f"--proxy-server={config.proxy}")
            
            options.add_argument(f"--window-size={config.window_size[0]},{config.window_size[1]}")
            
            if config.disable_images:
                prefs = {"profile.managed_default_content_settings.images": 2}
                options.add_experimental_option("prefs", prefs)
            
            self.driver = webdriver.Chrome(options=options)
        
        elif config.browser_type == BrowserType.FIREFOX:
            options = FirefoxOptions()
            
            if config.headless:
                options.add_argument("--headless")
            
            if config.user_agent:
                options.set_preference("general.useragent.override", config.user_agent)
            
            self.driver = webdriver.Firefox(options=options)
        
        elif config.browser_type == BrowserType.EDGE:
            options = EdgeOptions()
            
            if config.headless:
                options.add_argument("--headless")
            
            self.driver = webdriver.Edge(options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {config.browser_type}")
        
        # Set timeout
        self.driver.set_page_load_timeout(config.timeout)
    
    def _execute_action(self, action: BrowserAction, context: Dict[str, Any]) -> Any:
        """
        Execute single browser action
        
        Args:
            action: Action to execute
            context: Context variables for string interpolation
            
        Returns:
            Action result (if any)
        """
        result = None
        
        # Replace variables in target and value
        target = action.target.format(**context) if action.target else None
        value = action.value.format(**context) if action.value else None
        
        if action.action_type == ActionType.NAVIGATE:
            self.driver.get(target)
            result = self.driver.current_url
        
        elif action.action_type == ActionType.CLICK:
            # Try multiple selector strategies
            element = None
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, target)
            except:
                try:
                    element = self.driver.find_element(By.XPATH, target)
                except:
                    pass
            
            if element:
                element.click()
                result = True
        
        elif action.action_type == ActionType.TYPE:
            element = None
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, target)
            except:
                try:
                    element = self.driver.find_element(By.XPATH, target)
                except:
                    pass
            
            if element:
                element.clear()
                element.send_keys(value)
                result = True
        
        elif action.action_type == ActionType.SCROLL:
            if value == "bottom":
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elif value == "top":
                self.driver.execute_script("window.scrollTo(0, 0);")
            elif value:
                self.driver.execute_script(f"window.scrollBy(0, {value});")
            result = True
        
        elif action.action_type == ActionType.WAIT:
            wait_time = float(value) if value else 1.0
            time.sleep(wait_time)
            result = True
        
        elif action.action_type == ActionType.SCREENSHOT:
            screenshot_path = self.output_dir / target
            self.driver.save_screenshot(str(screenshot_path))
            result = str(screenshot_path)
        
        elif action.action_type == ActionType.EXTRACT:
            elements = self.driver.find_elements(By.CSS_SELECTOR, target)
            result = [elem.text for elem in elements]
            
            # Store in context if extract_as specified
            if "extract_as" in action.metadata:
                context[action.metadata["extract_as"]] = result
        
        elif action.action_type == ActionType.EXECUTE_JS:
            result = self.driver.execute_script(value)
            
            # Store in context if extract_as specified
            if "extract_as" in action.metadata:
                context[action.metadata["extract_as"]] = result
        
        # Wait after action
        if action.wait_after > 0:
            time.sleep(action.wait_after)
        
        return result
    
    def run_workflow(self, workflow: Workflow, context: Optional[Dict[str, Any]] = None) -> SessionResult:
        """
        Execute complete workflow
        
        Args:
            workflow: Workflow to execute
            context: Context variables for actions
            
        Returns:
            SessionResult with execution details
        """
        session_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        # Add timestamp to context
        if context is None:
            context = {}
        context["timestamp"] = start_time.strftime("%Y%m%d_%H%M%S")
        context["session_id"] = session_id
        
        result = SessionResult(
            session_id=session_id,
            workflow_name=workflow.name,
            status=SessionStatus.RUNNING,
            start_time=start_time
        )
        
        try:
            # Create browser
            self._create_driver(workflow.config)
            
            # Execute actions
            for action in workflow.actions:
                try:
                    action_result = self._execute_action(action, context)
                    result.actions_completed += 1
                    
                    # Collect screenshots
                    if action.action_type == ActionType.SCREENSHOT and action_result:
                        result.screenshots.append(action_result)
                
                except Exception as e:
                    result.actions_failed += 1
                    print(f"Action failed: {action.action_type.value} - {e}")
            
            # Store extracted data from context
            for key, value in context.items():
                if key not in ["timestamp", "session_id", "url"]:
                    result.extracted_data[key] = value
            
            result.status = SessionStatus.COMPLETED if result.actions_failed == 0 else SessionStatus.FAILED
        
        except Exception as e:
            result.status = SessionStatus.FAILED
            result.error_message = str(e)
        
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
            
            result.end_time = datetime.now()
        
        return result
    
    def close(self):
        """Close browser if still open"""
        if self.driver:
            self.driver.quit()
            self.driver = None


def demo_automation():
    """Demo mode: Simple browser automation example"""
    print("🤖 Web Automation Framework Demo\n")
    print("=" * 60)
    
    if not SELENIUM_AVAILABLE:
        print("\n❌ Selenium not installed")
        print("   Install with: pip install selenium")
        print("\n   Demo cannot proceed without Selenium.")
        return
    
    # Create simple workflow
    from models import Workflow, BrowserAction, BrowserConfig, ActionType, BrowserType
    
    workflow = Workflow(
        name="Demo Workflow",
        description="Navigate to example.com and capture screenshot",
        actions=[
            BrowserAction(ActionType.NAVIGATE, target="https://example.com"),
            BrowserAction(ActionType.WAIT, value="2"),
            BrowserAction(ActionType.SCREENSHOT, target="demo_{timestamp}.png"),
            BrowserAction(ActionType.EXECUTE_JS, 
                         value="return document.title;",
                         metadata={"extract_as": "title"})
        ],
        config=BrowserConfig(browser_type=BrowserType.CHROME, headless=True)
    )
    
    print("\n[1/3] Workflow Configuration")
    print(f"   Name: {workflow.name}")
    print(f"   Actions: {len(workflow.actions)}")
    print(f"   Browser: {workflow.config.browser_type.value}")
    print(f"   Headless: {workflow.config.headless}")
    
    print("\n[2/3] Executing workflow...")
    
    try:
        engine = AutomationEngine()
        result = engine.run_workflow(workflow)
        
        print(f"   ✅ Session: {result.session_id[:8]}")
        print(f"   Status: {result.status.value}")
        print(f"   Actions completed: {result.actions_completed}")
        print(f"   Duration: {result.duration:.2f}s")
        
        if result.screenshots:
            print(f"   Screenshots: {len(result.screenshots)}")
            for screenshot in result.screenshots:
                print(f"      - {screenshot}")
        
        if result.extracted_data:
            print(f"   Extracted data:")
            for key, value in result.extracted_data.items():
                print(f"      {key}: {value}")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n[3/3] Demo complete!")
    print("\n" + "=" * 60)
