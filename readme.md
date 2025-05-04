# Weekly Menu & Grocery List Generator

Welcome to the **Weekly Menu & Grocery List Generator**! This is a simple web application where you can add dishes you know, create a weekly menu, and automatically generate a grocery list based on the selected menu. It's designed to make your meal planning easier and help you organize your grocery shopping!

## Features
- **Add Dishes**: Store and manage the dishes you know with all the necessary ingredients.
- **Create Weekly Menu**: Select dishes for each day of the week and plan your meals.
- **Automatic Grocery List Generation**: Based on your selected menu, the app will automatically generate a grocery list with the necessary ingredients for the entire week.

## Tech Stack
This application uses the following technologies:
- **Flask**: A lightweight Python web framework for building the application.
- **SQLite**: A simple and efficient relational database to store dishes and their ingredients.
- **Bootstrap**: A popular CSS framework to make the website responsive and visually appealing.

## Installation

### Prerequisites
Make sure you have the following installed on your machine:
- Python 3.12
- Flask
- SQLite

### Steps to Run the Project Locally

1. **Clone the repository**:
    ```bash
    git clone https://github.com/NickHemerycke/NomNomicon.git
    ```

2. **Install dependencies**:
    Install the required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    After installing the dependencies, start the Flask development server:
    ```bash
    flask run
    ```
    The app will be running at `http://127.0.0.1:5000`.


5. **Start Adding Dishes**:
    Visit the app at `http://127.0.0.1:5000` and begin adding your dishes and planning your weekly menu!

6. **future implementations**:
    user authentication, frontend framework and ...

## Contributing
If you'd like to contribute to this project, feel free to fork the repository, make changes, and create a pull request. Contributions, issues, and suggestions are always welcome!

## License
This project is open-source and available under the [MIT License](LICENSE).
