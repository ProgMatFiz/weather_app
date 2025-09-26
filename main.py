from data_collection.html_data_collection import HtmlDataCollection
from gui.qt_view import GUI
from app.controller import Controller


def main():
    # Defining the model view and controller
    model = HtmlDataCollection()
    view = GUI()
    Controller(view, model)

    # Running the GUI
    view.run_app()


if __name__ == "__main__":
    main()
