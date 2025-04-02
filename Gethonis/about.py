import time
import asyncio
import reflex as rx

from . import ai
from random import randint
from rxconfig import config
from . import about as ap

def aboutpage() -> rx.Component:
	return rx.container(
		rx.desktop_only(
			rx.box(
			rx.center(
				rx.heading("About this project", font_size="50px"),
			),
			rx.center(
				rx.link("Go back", href="/"),
				padding="30px"
			),
			rx.center(
				rx.text(""" This project is simply a combination of DeepSeek and ChatGPT-4. The main idea is that the prompt is sent to OpenAI first and then to DeepSeek. Both answers are collected and combined into a single response. The task specified to either OpenAI or DeepSeek is: 'Compare these responses, correct any mistakes, and provide an improved answer—just the answer, not the comparison.' Along with this task, include answer 1 and answer 2."""),
				padding="5em",
				text_align="center",
				padding_top="5em",
			),
			rx.center(
				rx.grid(
					rx.card(
						rx.center(
							rx.heading("Designer"),
						),
						rx.center(
							rx.badge(
								rx.heading("Georgiana", size="6")
							),
							padding="20px"
						),
						rx.center(
							#rx.link(rx.icon("github"), href="https://github.com/", variant="ghost")
						),
						padding="20px"
					),
					rx.card(
						rx.center(
							rx.heading("Coder"),
						),
						rx.center(
							rx.badge(
								rx.heading("Lucian", size="6")
							),
							padding="20px"
						),
						rx.center(
							#rx.link(rx.icon("github"), href="https://github.com/lucian-xinitrc", variant="ghost")
						),
						padding="20px"
					),
					columns="2",
					spacing="5"
				)
			),
			rx.center(
				rx.text("""Above is a brief introduction to the creators of this website: first, my sweet girlfriend, who designed the concept, and then me—the developer and author of this project."""),
				padding="5em",
				text_align="center",
			),
			padding_top="5em"
			)
		),
		rx.mobile_and_tablet(
			rx.box(
			rx.center(
				rx.heading("About this project", font_size="50px"),
			),
			rx.center(
				rx.link("Go back", href="/"),
				padding="30px"
			),
			rx.center(
				rx.text("""This project is simply a combination of DeepSeek and ChatGPT-4. The main idea is that the prompt is sent to OpenAI first and then to DeepSeek. Both answers are collected and combined into a single response. The task specified to either OpenAI or DeepSeek is: 'Compare these responses, correct any mistakes, and provide an improved answer—just the answer, not the comparison.' Along with this task, include answer 1 and answer 2."""),
				padding="5em",
				text_align="center",
				padding_top="5em",
			),
			rx.center(
				rx.grid(
					rx.card(
						rx.center(
							rx.heading("Designer"),
						),
						rx.center(
							rx.badge(
								rx.heading("Georgiana", size="6")
							),
							padding="20px"
						),
						rx.center(
							#rx.link(rx.icon("github"), href="https://github.com/", variant="ghost")
						),
						padding="20px"
					),
					rx.card(
						rx.center(
							rx.heading("Coder"),
						),
						rx.center(
							rx.badge(
								rx.heading("Lucian", size="6")
							),
							padding="20px"
						),
						rx.center(
							#rx.link(rx.icon("github"), href="https://github.com/lucian-xinitrc", variant="ghost")
						),
						padding="20px"
					),
					rows="2",
					spacing="5"
				)
			),
			rx.center(
				rx.text("""Above is a brief introduction to the creators of this website: first, my sweet girlfriend, who designed the concept, and then me—the developer and author of this project."""),
				padding="5em",
				text_align="center",
			),
			padding_top="5em"
		)
		)
	)	