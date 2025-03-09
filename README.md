# Project Setup

This project requires Python 3.12. Follow these steps to set up your environment:

1.  **Create a Virtual Environment:**
    ```bash
    python3.12 -m venv .venv
    ```

2.  **Activate the Virtual Environment:**

    * **macOS and Linux:**
        ```bash
        source .venv/bin/activate
        ```
    * **Windows:**
        ```bash
        .venv\Scripts\activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    (Ensure you have a `requirements.txt` file in the same directory, containing:
    ```
    mediapipe
    opencv-python
    numpy
    ```
    )

Now you're ready to run the project!
