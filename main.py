from data_collection.html_data_collection import HtmlDataCollection
from gui.qt_view import GUI
from app.controller import Controller


def main():
    model = HtmlDataCollection()
    view = GUI()
    Controller(view, model)
    view.run_app()


if __name__ == "__main__":
    main()
