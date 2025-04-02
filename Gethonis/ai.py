#!/usr/bin/env python3

import os, openai, dotenv
from random import randint
from dotenv import load_dotenv
from openai import OpenAI

class ArtificialIntelligence:
	messages = [{"role": "system", "content": "You are a helpful assistant"}]
	def __init__(self, token, model, baseUrl, type):
		load_dotenv()
		self.token = token
		self.model = model
		self.baseUrl = baseUrl
		self.type = type

	def getMessage(self, message) -> str:
		try:
			if self.type == True:
				client = OpenAI(api_key=self.token)
			else:
				client = OpenAI(api_key=self.token, base_url=self.baseUrl)
			self.messages.append({"role": "user", "content": message})
			response = client.chat.completions.create(
			    model=self.model,
			    messages=self.messages,
			    stream=False
			)
			self.messages.append(response.choices[0].message)
			return response.choices[0].message.content
		except:
			return "Error at messaging!"

class Integration(ArtificialIntelligence):
	def __init__(self):
		load_dotenv()
		self.Open = ArtificialIntelligence(
			os.getenv('tokenOpen'),
			os.getenv('modelOpen'),
			os.getenv('baseUrlOpen'),
			True
		)
		self.Deep = ArtificialIntelligence(
			os.getenv('tokenDeep'),
			os.getenv('modelDeep'),
			os.getenv('baseUrlDeep'), 
			False
		)

	def Gethonis(self, message, option, subOption, ran):
		action = "Compare those, solve mistakes and give it better, Just the answer not the comparation."
		try:
			ResponseOpen = self.Open.getMessage(message)
		except:
			return "Error at OpenAI Message!"

		try:
			ResponseDeep = self.Deep.getMessage(message)
		except:
			return "Error at DeepSeek Message!"

		if option == 3:
			which = ran
			if which == 0:
				#print("ChatGPT")
				return self.Open.getMessage(action + " " + ResponseOpen + " " + ResponseDeep)
			elif which == 1:
				#print("DeepSeek")
				return self.Deep.getMessage(action + " " + ResponseOpen + " " + ResponseDeep)
		elif option == 4:
			if subOption == 1:
				return self.Open.getMessage(action + " " + ResponseOpen + " " + ResponseDeep)
			elif subOption == 2:
				return self.Deep.getMessage(action + " " + ResponseOpen + " " + ResponseDeep)
			elif option is None:
				pass

	def OpenAI(self, message):
		return self.Open.getMessage(message)

	def DeepSeek(self, message):
		return self.Deep.getMessage(message)


class Initiate(Integration):
	def __init__(self, dict, ran):
		load_dotenv()
		self.obj = Integration()
		self.option= dict['Type']
		self.message = dict['Message']
		self.response = self.Gethonised(self.option, self.message, ran)

	def getting_messages(self, message, option, ran) -> str:
		try:
			if(message == "Exit"):
				return "Exiting"
		except:
			return "Error at input."
		try:
			if option == 3:
				return self.obj.Gethonis(message, 3, 0, ran)
			elif option == 2:
				return self.obj.OpenAI(message)
			elif option == 1:
				return self.obj.DeepSeek(message)
		except:
			return "Error at Integration"

	def Gethonised(self, option, message, ran):
		if option == "Gethonis":
			return self.getting_messages(message, 3, ran)
		elif option == "OpenAI":
			return self.getting_messages(message, 2, ran)
		elif option == "DeepSeek":
			return self.getting_messages(message, 1, ran)
		else:
			return "Wrong Option"


