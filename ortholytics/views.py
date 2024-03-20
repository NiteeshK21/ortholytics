from django.shortcuts import render, redirect
# from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from .models import *
### new added 
from django.http import HttpResponse
from django.http import JsonResponse
import pymongo
import pandas as pd
import numpy as np
import json


from .models import collection  ## pymongo db collection
import pandas as pd
from datetime import datetime
import assemblyai as aai
import json
import requests
from datetime import date

# Replace with your API key

   
def transform_mongo_data(result):
  results_list = []
  for document in result:
      results_list.append(document)
  return results_list

def eachfile(request):
    # if request.is_ajax() and request.method == 'POST':
        # Get the input data from the AJAX request
        name = request.GET.get('name')
        interactions_schedule=db['interactions']
        query = {'file_name': name}
        result=interactions_schedule.find(query,{"_id":0})
        result=transform_mongo_data(result)
        print(result[0])
        print("Nameeeeeee:",name)
        # Process the input data (you can perform any necessary operations here)
        context={
            "files":json.dumps(result[0])
        }
        # Render the new HTML page with any context data
        return render(request, 'eachfile.html', context)
    # else:
    #     # Handle non-ajax requests or other methods
    #     return JsonResponse({'error': 'Invalid request'})
    # interactions_schedule=db['interactions']
    # result=interactions_schedule.find("",{"_id":0})
    # result=transform_mongo_data(result)
    # context={
    #     "files":json.dumps(result)
    # }
    # return render(request, "dashboard.html", context)

def dashboard(request):
    interactions_schedule=db['interactions']
    result=interactions_schedule.find("",{"_id":0})
    result=transform_mongo_data(result)
    context={
        "files":json.dumps(result)
    }
    return render(request, "dashboard.html", context)
def files(request):
    interactions_schedule=db['interactions']
    result=interactions_schedule.find("",{"_id":0})
    result=transform_mongo_data(result)
    df=pd.DataFrame(result)
    print(df)
    # print(result)
    for val in result:
        print(val['file_name'])
    context={
         "files":json.dumps(result)
      }
    return render(request, "files.html", context)

def diarization(audio_file):
    print(audio_file)
    print("Dekho mai yaha aayaaaaaaaaa!")
    aai.settings.api_key = "0ca2f9180fdc4dfeb7e2831d8201da1b"
    FILE_URL=audio_file
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
    FILE_URL,
    config=config
    )
    text=""
    for utterance in transcript.utterances:
        text+=f"Speaker {utterance.speaker}: {utterance.text}"
    return text

def chat(user):
    print(user)
#     user+="""Analyze the provided conversation between a customer and a support agent to gain insights into various aspects related to the product. Specifically, focus on the following topics:

# Customer Experience:

# Evaluate the overall satisfaction level of the customer with the product.
# Identify any positive aspects of the product highlighted by the customer.
# Determine if there are any areas where the customer is experiencing challenges or dissatisfaction.
# Competitor Analysis:

# Investigate whether the customer mentions any competitors or alternative solutions.
# Explore any specific features or qualities of the competitor that the customer finds appealing or superior.
# Assess how the customer perceives the product in comparison to its competitors.
# Issue Identification:

# Identify any issues or pain points mentioned by the customer regarding the product.
# Determine the severity and frequency of these issues.
# Look for patterns or common themes among the reported issues.
# Expense Management:

# Determine if there are any references to the cost or value of the product.
# Assess whether the customer perceives the product as cost-effective or if they mention any concerns about pricing.
# Frequency of Interactions:

# Analyze how often the customer interacts with the support agent or reaches out for assistance.
# Consider whether the frequency of interactions indicates a high level of engagement or potential issues with the product.
# Suggestions from Customer:

# Review any suggestions or feedback provided by the customer for improving the product.
# Assess the feasibility and relevance of these suggestions in enhancing the customer experience and addressing any identified issues."""
    # prompt="""Given the following information, generate a JSON file containing the key and classify the customer text into a specific category based on the conversation. Do not return the text. \n\n\"Text\"\n\nPositive Feedback Categories: Categories the customer Text in one of the following class [Appreciation Satisfaction Praise Ease of Use Helpful Speed Efficiency Quality Value Reliability Innovation Personalization]\n\nNegative Feedback Categories: Categories the customer Text in one of the following class [Frustration Dissatisfaction Complaints Confusion Inefficiency Poor Quality Technical Issues Accessibility Problems Usability Concerns Lack of Features Performance Issues Billing Problems]\n\nNegative Feedback - Constructive Categories: Categories the customer Text in one Specific class of the following class [Suggestions Improvements Enhancements Feature Requests Bug Reports Usability Recommendations Workflow Suggestions Training Needs Documentation Issues Policy Changes]\n\nCompetitor Performance Categories: Categories the customer Text in one of the following class [Speed Features Usability Customer Support Price Reliability Innovation Market Presence Brand Reputation Customization Options Integration Capabilities]\n\nList of Products: Categories the customer Text in one of the following class [Platform Software Application Service Tool Solution Device System Appliance Equipment Program Feature]\n\nList of Conversation Topics between Customer and Agent: Categories the customer Text in one of the following class [Account Access Billing Inquiries Technical Support Product Information Feature Requests Complaints Feedback Training Needs Order Status Returns and Refunds Troubleshooting Subscription Management]\n\nDifferent Possible Issues Classes: Categories the customer Text in one of the following class [Technical Issues Account Problems Billing Errors Service Interruptions Performance Degradation Accessibility Challenges Usability Concerns Product Defects Policy Violations Security Breaches Communication Problems Integration Issues"""
    # prompt="""Given the provided information, create a JSON file containing the key and classify the customer's text into a specific category based on the conversation. Do not include the actual text.\n\nPositive Feedback Categories: Classify the customer's text into one of the following categories: Satisfaction, Ease of Use, Helpfulness, Efficiency, Quality, Value, Reliability, Innovation, Personalization, Responsiveness.\n\nNegative Feedback Categories: Classify the customer's text into one of the following categories: Frustration, Dissatisfaction, Complaints, Confusion, Inefficiency, Poor Quality, Technical Issues, Accessibility Problems, Usability Concerns, Lack of Features, Performance Issues, Billing Problems.\n\nNegative Feedback - Constructive Categories: Classify the customer's text into one of the following specific categories: Suggestions, Improvements, Enhancements, Feature Requests, Usability Recommendations, Workflow Suggestions, Training Needs, Documentation Issues, Policy Changes.\n\nCompetitor Performance Categories: Classify the customer's text into one of the following categories: Speed, Features, Usability, Customer Support, Price, Reliability, Innovation, Market Presence, Brand Reputation, Customization Options, Integration Capabilities.\n\nList of Products: Classify the customer's text into one of the following categories: Platform, Software, Application, Service, Tool, Solution, Device, System, Appliance, Equipment, Program, Feature.\n\nList of Conversation Topics between Customer and Agent: Classify the customer's text into one of the following categories: Account Management, Billing and Payments, Technical Support, Product Information, Feature Requests, Complaints Handling, Feedback Collection, Training and Education, Order Management, Returns and Refunds, Troubleshooting, Subscription Management.\n\nDifferent Possible Issues Classes: Classify the customer's text into one of the following categories: Technical Issues, Account Problems, Billing Errors, Service Interruptions, Performance Degradation, Accessibility Challenges, Usability Concerns, Product Defects, Policy Violations, Security Concerns, Communication Problems, Integration Issues."""
    # prompt+="Conversation:"+user
#     user+="""1. Classify User from text into - Power User , Weak User , Intermidiate User 
# 2. Extract and classify instances or phrases or lines spoken as positive, negative, constructive.
# 5. Extract Point on which Competitor is Preforming well in one word .
# 6 Extract the Product which customer is using 
# 7. Give one word topic for conversation 
# 8  Classifiy Issue in one class
# 9  Classfify Resolution in one category"""
    inst="""Analyze the provided conversation between a customer and a support agent to gain insights into various aspects related to the product. Specifically, focus on the following topics:

Customer Experience:

Evaluate the overall satisfaction level of the customer with the product.
Identify any positive aspects of the product highlighted by the customer.
Determine if there are any areas where the customer is experiencing challenges or dissatisfaction.
Competitor Analysis:

Investigate whether the customer mentions any competitors or alternative solutions.
Explore any specific features or qualities of the competitor that the customer finds appealing or superior.
Assess how the customer perceives the product in comparison to its competitors.
Issue Identification:

Identify any issues or pain points mentioned by the customer regarding the product.
Determine the severity and frequency of these issues.
Look for patterns or common themes among the reported issues.
Suggestions from Customer:

Review any suggestions or feedback provided by the customer for improving the product.
Assess the feasibility and relevance of these suggestions in enhancing the customer experience and addressing any identified issues.
Keep the response short and breif while making sure that no information is missed.
Use strong and impactful words, but make sure misinformation does not happen."""
    prompt=f"""
      "text": {user},
  "instructions": f"{inst}
"""
    url = "https://api.edenai.run/v2/text/chat"
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTY2ZDAyMTQtODlmNi00Y2UyLWI0MTYtNGEyZjMxNmNkMGZkIiwidHlwZSI6ImFwaV90b2tlbiJ9.SRJr5Er6nU8J2BKNZAgtWAHCS2n8x-O7wVAp_bN4_Tk"}
    payload = {
        "providers":"openai",
        "model":"gpt-4",
        "text": prompt,
        "chatbot_global_action": "You are an expert data analyst.",
        "previous_history": [],
        "temperature": 0.2,
        "max_tokens": 1000,
        "fallback_providers": ""
        
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    # print(result)
    # print(result['openai']['generated_text'])
    return result['openai']['generated_text']

def eval(text):
    inst="Given the provided information, create a JSON file containing the key and classify the customer's text into a specific category based on the conversation. Do not include the actual text.\n\nPositive Feedback Categories: Classify the customer's text into one of the following categories: Satisfaction, Ease of Use, Helpfulness, Efficiency, Quality, Value, Reliability, Innovation, Personalization, Responsiveness.\n\nNegative Feedback Categories: Classify the customer's text into one of the following categories: Frustration, Dissatisfaction, Complaints, Confusion, Inefficiency, Poor Quality, Technical Issues, Accessibility Problems, Usability Concerns, Lack of Features, Performance Issues, Billing Problems.\n\nNegative Feedback - Constructive Categories: Classify the customer's text into one of the following specific categories: Suggestions, Improvements, Enhancements, Feature Requests, Usability Recommendations, Workflow Suggestions, Training Needs, Documentation Issues, Policy Changes.\n\nCompetitor Performance Categories: Classify the customer's text into one of the following categories: Speed, Features, Usability, Customer Support, Price, Reliability, Innovation, Market Presence, Brand Reputation, Customization Options, Integration Capabilities.\n\nList of Products: Classify the customer's text into one of the following categories: Platform, Software, Application, Service, Tool, Solution, Device, System, Appliance, Equipment, Program, Feature.\n\nList of Conversation Topics between Customer and Agent: Classify the customer's text into one of the following categories: Account Management, Billing and Payments, Technical Support, Product Information, Feature Requests, Complaints Handling, Feedback Collection, Training and Education, Order Management, Returns and Refunds, Troubleshooting, Subscription Management.\n\nDifferent Possible Issues Classes: Classify the customer's text into one of the following categories: Technical Issues, Account Problems, Billing Errors, Service Interruptions, Performance Degradation, Accessibility Challenges, Usability Concerns, Product Defects, Policy Violations, Security Concerns, Communication Problems, Integration Issues."
    prompt=text+inst
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTY2ZDAyMTQtODlmNi00Y2UyLWI0MTYtNGEyZjMxNmNkMGZkIiwidHlwZSI6ImFwaV90b2tlbiJ9.SRJr5Er6nU8J2BKNZAgtWAHCS2n8x-O7wVAp_bN4_Tk"}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers":"openai",
        "model":"gpt-4",
        "text": prompt,
        "chatbot_global_action": "You are an expert data analyst.",
        "previous_history": [],
        "temperature": 0.2,
        "max_tokens": 1000,
        "fallback_providers": ""
    }
    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    # print(result['openai']['generated_text'])
    data=result['openai']['generated_text']
    data=data.strip("`")
    print(data)
    dataa=json.loads(data)
    # dataa=dict(data)
    return dataa

def calculate_feedback_ratio(json_data):
    # Extract positive feedback categories and negative feedback categories
    positive_feedback_categories = json_data.get('categories', {}).get('positive_feedback', [])
    negative_feedback_constructive_categories = json_data.get('categories', {}).get('negative_feedback_constructive', [])
    negative_feedback_categories = json_data.get('categories', {}).get('negative_feedback', [])

    ratio = (len(positive_feedback_categories) + len(negative_feedback_constructive_categories)) / ((1+len(positive_feedback_categories) + len(negative_feedback_categories) + len(negative_feedback_constructive_categories)))

    return ratio * 100

def type(conversation):
    inst="Classify the user's proficiency level based on the conversation. The possible levels are: 'Power User,' 'Weak User,' and 'Intermediate User.' Return a single string from this list that best represents the user's proficiency level in the given conversation. Don't write extra text just return key word from list no other character or word to be returned ."
    prompt=conversation+inst
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTY2ZDAyMTQtODlmNi00Y2UyLWI0MTYtNGEyZjMxNmNkMGZkIiwidHlwZSI6ImFwaV90b2tlbiJ9.SRJr5Er6nU8J2BKNZAgtWAHCS2n8x-O7wVAp_bN4_Tk"}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers":"openai",
        "model":"gpt-4",
        "text": prompt,
        "chatbot_global_action": "You are an expert data analyst.",
        "previous_history": [],
        "temperature": 0.2,
        "max_tokens": 1000,
        "fallback_providers": ""
    }
    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    return result['openai']['generated_text']

def index(request):
    name="Conversation2"
    summary = chat(conversation)    
    parameters = eval(conversation)
    # parameters=parameters.strip()
    # parameters=parameters[4:]
    # print(parameters)
    # parameters=json.loads(parameters)
    # parameters=parameters["CustomerFeedback"]
    score = calculate_feedback_ratio(parameters)
    user_type=type(conversation)
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    interactions_schedule=db['interactions']
    data={
        "file_name":name,
        "date":today,
        "score":score,
        "UserType":user_type,
        "conversation":conversation,
        "summary":summary,
        "parameters":parameters
    }
    print(data)
    interactions_schedule.insert_one(data)
    # if request.method == 'POST':
    #     if request.FILES['audioFile']:
    #         audio_file = request.FILES['audioFile']
    #         print(audio_file)
    #         # with open('temp_audio.wav', 'wb') as f:
    #         #     for chunk in audio_file.chunks():
    #         #         f.write(chunk)
    #         # print(audio_file.name)
    #         # conversation=diarization('temp_audio.wav')
    #         global conversation
    #         # global modified
    #         # if(modified!=1):
    #         # conversation=conversation.replace("Speaker", "\n\nSpeaker")
    #         # conversation=conversation[2:]
    #         # modified=1
    #         summary = chat(conversation)
    #         parameters = eval(conversation)
    #         score = calculate_feedback_ratio(parameters)
    #         today = date.today()
    #         today = today.strftime("%d/%m/%Y")
    #         interactions_schedule=db['interactions']
    #         data={
    #             "file_name":audio_file.name,
    #             "date":today,
    #             "score":score,
    #             "conversation":conversation,
    #             "summary":summary,
    #             "parameters":parameters
    #         }
    #         print(data)
    #         interactions_schedule.insert_one(data)
    #         # summary="dummy summary"
    #         return JsonResponse({'conversation': conversation,
    #                              "summary":summary})
    #     else:
    #         return JsonResponse({'error': 'Invalid request'}, status=400)
    context={
    }
    return render(request, "home.html", context)






# modified=0
conversation="""Speaker A: Welcome to our rental vehicle customer support. My name is Wendy. How can I assist you today?
Speaker B: Hi Wendy, I'm having trouble with your website. I encountered a bug while trying to book a car.
Speaker A: I apologize for the inconvenience. Could you please provide more details about the bug you encountered?
Speaker B: Sure, whenever I try to select a pickup location, the dropdown menu doesn't display any options. It's preventing me from proceeding with my reservation.
Speaker A: I'm sorry to hear that. Let me escalate this bug report to our technical team for immediate investigation and resolution.
Speaker B: Thank you. In addition to the bug, I also have some usability recommendations. The layout of your website is confusing, and it's difficult to navigate through the booking process.
Speaker A: Your feedback is valuable to us. We'll review your usability recommendations and work on enhancing the user experience of our website.
Speaker B: I appreciate that. I also have some feature requests to suggest improvements for the booking system.
Speaker A: Please share your feature requests with us. We're always looking for ways to enhance our services and meet the needs of our customers.
Speaker B: Lastly, I've been dissatisfied with the price of your rentals compared to your competitors. Your prices seem higher, and I'm considering using a different rental service.
Speaker A: I understand your concern about pricing. We continuously evaluate our pricing strategies to remain competitive in the market. Is there anything specific I can assist you with regarding pricing or booking?
Speaker B: Not at the moment, thank you. I appreciate your assistance, Wendy.
Speaker A: You're welcome. If you have any further questions or need assistance in the future, feel free to reach out to us. We're here to help.
"""