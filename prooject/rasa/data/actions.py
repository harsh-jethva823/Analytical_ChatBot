# # actions.py
# from rasa_sdk import Action
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.types import DomainDict
# from rasa_sdk.events import SlotSet
#
# class ActionProvideCourseFees(Action):
#     def name(self) -> str:
#         return "action_provide_course_fees"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker,
#             domain: DomainDict):
#         # Example logic
#         course = tracker.get_slot("course")
#         if course == "computer science":
#             fees = "INR 1,20,000 per year"
#         else:
#             fees = "Please specify a valid course."
#         dispatcher.utter_message(text=f"The fees for {course} is {fees}.")
#         return []
