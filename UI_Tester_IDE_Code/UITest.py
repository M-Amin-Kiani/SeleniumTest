from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time


class TodoAppTests(unittest.TestCase):
    URL = "https://todolist.james.am/"

    def setUp(self):
        """Set up the browser before each test."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.URL)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()

    def add_tasks(self, tasks):
        """Helper function to add multiple tasks."""
        input_box = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.new-todo"))
        )
        for task in tasks:
            input_box.send_keys(task + Keys.RETURN)
            time.sleep(1)  # Delay after adding each task

    def test_add_to_do(self):
        """Test adding tasks and verifying their count."""
        driver = self.driver
        tasks = ["task 1", "task 2", "task 3"]
        self.add_tasks(tasks)

        # Verify the number of tasks added
        time.sleep(2)  # Delay before verification
        list_items = driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li")
        self.assertEqual(len(list_items), len(tasks),
                         f"Expected {len(tasks)} tasks, but found {len(list_items)}")

    def test_check_items_left(self):
        """Test the remaining items count."""
        driver = self.driver
        tasks = ["task 1", "task 2", "task 3"]
        self.add_tasks(tasks)

        # Complete one task
        first_task_checkbox = driver.find_element(By.CSS_SELECTOR, "ul.todo-list li:first-child .toggle")
        first_task_checkbox.click()
        time.sleep(2)  # Delay after clicking checkbox

        # Verify the remaining tasks count
        remaining_count = driver.find_element(By.CSS_SELECTOR, "footer.footer .todo-count strong").text
        self.assertEqual(int(remaining_count), len(tasks) - 1,
                         f"Expected remaining count to be {len(tasks) - 1}, but found {remaining_count}")

    def test_check_filter(self):
        """Test filtering tasks by 'active' and 'completed'."""
        driver = self.driver
        tasks = ["task 1", "task 2", "task 3"]
        self.add_tasks(tasks)

        # Complete some tasks
        driver.find_element(By.CSS_SELECTOR, "ul.todo-list li:first-child .toggle").click()
        time.sleep(1)  # Delay after completing a task
        driver.find_element(By.CSS_SELECTOR, "ul.todo-list li:last-child .toggle").click()
        time.sleep(1)

        # Check active filter
        driver.find_element(By.CSS_SELECTOR, 'ul.filters li a[href="#/active"]').click()
        time.sleep(2)  # Delay after switching to active filter
        active_todos = driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li")
        active_texts = [todo.text for todo in active_todos]
        self.assertEqual(active_texts, ["task 2"], "Active filter did not return correct tasks.")

        # Check completed filter
        driver.find_element(By.CSS_SELECTOR, 'ul.filters li a[href="#/completed"]').click()
        time.sleep(2)  # Delay after switching to completed filter
        completed_todos = driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li")
        completed_texts = [todo.text for todo in completed_todos]
        self.assertEqual(set(completed_texts), {"task 1", "task 3"},
                         "Completed filter did not return correct tasks.")

    def test_delete_item(self):
        """Test deleting a task."""
        driver = self.driver
        tasks = ["task 1", "task 2", "task 3"]
        self.add_tasks(tasks)

        # Delete the first task
        first_task = driver.find_element(By.CSS_SELECTOR, "ul.todo-list li:first-child")
        delete_button = first_task.find_element(By.CSS_SELECTOR, "button.destroy")
        driver.execute_script("arguments[0].click();", delete_button)
        time.sleep(2)  # Delay after deleting task

        # Verify the task is deleted
        remaining_tasks = driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li label")
        remaining_texts = [task.text for task in remaining_tasks]
        self.assertNotIn("task 1", remaining_texts, "Task 'task 1' was not deleted.")

    def test_clear_completed(self):
        """Test clearing all completed tasks."""
        driver = self.driver
        tasks = ["task 1", "task 2", "task 3"]
        self.add_tasks(tasks)

        # Complete all tasks
        toggles = driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li .toggle")
        for toggle in toggles:
            toggle.click()
            time.sleep(1)  # Delay after completing each task

        # Clear completed tasks
        driver.find_element(By.CSS_SELECTOR, "button.clear-completed").click()
        time.sleep(2)  # Delay after clearing tasks

        # Verify all tasks are cleared
        remaining_tasks = driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li")
        self.assertEqual(len(remaining_tasks), 0, "Completed tasks were not cleared.")

    def test_toggle_all(self):
        """Test toggling all tasks as completed."""
        driver = self.driver
        tasks = ["task 1", "task 2", "task 3"]
        self.add_tasks(tasks)

        # Use JavaScript to click the toggle-all checkbox to avoid interception
        toggle_all = driver.find_element(By.CSS_SELECTOR, "input#toggle-all")
        driver.execute_script("arguments[0].click();", toggle_all)

        # Wait a moment to allow UI updates
        import time
        time.sleep(2)

        # Verify all tasks are marked as completed
        completed_todos = driver.find_elements(By.CSS_SELECTOR, "ul.todo-list li.completed")
        self.assertEqual(len(completed_todos), len(tasks),
                         "Not all tasks were marked as completed.")


if __name__ == "__main__":
    unittest.main()