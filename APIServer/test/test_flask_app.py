from unittest import TestCase, main
from APIServer.flask_app import app, HelloWorld, Models, Props, Menu
from flask_restplus import Resource, Api, fields
import json


class HelloWorldTest(TestCase):
    def setUp(self):
        self.HelloWorld = HelloWorld(Resource)
        self.Model = Models(Resource)
        self.Props = Props(Resource)
        self.Menu = Menu(Resource)

    def test_HelloWorld(self):
        """
        See if HelloWorld works.
        """
        rv = self.HelloWorld.get()
        self.assertEqual(rv, {'hello': 'world'})

    def test_Get_Model(self):
        """
        See if we can get models.
        """
        rv = self.Model.get()
        self.assertEqual(type(rv), list)

    def test_Get_Props(self):
        """
        See if we can get props.
        """
        model_id = 1
        rv = self.Props.get(model_id)
        self.assertEqual(type(rv), dict)
        
    def test_Get_Menu(self):
        """
        Testing whether we are getting the menu.
        """
        model_id = 1
        rv = self.Menu.get(model_id)
        self.assertEqual(type(rv), list)
        
    def test_Put_Menu(self):
        """
        Testing whether we are able to put the menu in
        """
        menuitem_id = 1
        rv = self.Menu.put(menuitem_id)
        self.assertEqual(rv, {"execute menu item": menuitem_id, "Menu": "menu will be returned here"})
        

    # def test_Put_Props(self):
    #     """
    #     See if we can put props.
    #     """
    #     model_id = 1
    #     with app.app_context():
    #         rv = self.Props.put(model_id)
    #         self.assertEqual(rv, "Menu : menu will be returned here")
    #
    #     # with app.test_client() as c:
    #     #     rv = c.Props.put(model_id)
    #     #     self.assertEqual(rv, "Menu : menu will be returned here")
    #
    #     # rv = self.Props.put(model_id)
    #     # self.assertEqual(rv, "Menu : menu will be returned here")


if __name__ == "__main__":
    main()