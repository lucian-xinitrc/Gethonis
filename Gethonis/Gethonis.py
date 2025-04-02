import time
import asyncio
import reflex as rx

from . import ai
from random import randint
from rxconfig import config
from . import about


class State(rx.State):
    title = "Gethonis"
    value: str = "Gethonis"
    form_data: dict = {}
    messages: list[tuple[str, str]]
    show_chat = False
    height = 0 
    i = 0
    margin = "10%"
    margin_mobile = "50%"
    margin_top = "70%"
    margin_top_tab = "30%"
    dots: str = "..."
    response: str

    @rx.event
    async def handle_submit(self, form_data: dict):
        self.i = self.i + 1
        self.show_chat = True
        self.height = 500
        self.margin = "0%"
        self.margin_mobile = "0%"
        self.margin_top = "0%"
        self.margin_top_tab = "0%"
        self.form_data = form_data
        ran = randint(0, 1)
        if(form_data["Type"] == "Gethonis"):
            if ran == 0:
                model = "ChatGPT"
            else: 
                model = "DeepSeek"
        else:
            model = form_data["Type"]

        self.messages.append((form_data["Message"], model, "Thinking..."))
        yield        
        await asyncio.create_task(self.process_response(form_data, model, ran))
        self.change_messages(self.messages, 0, form_data["Message"], self.response, model)

    async def process_response(self, form_data: dict, model: str, ran: int):
        self.response = await asyncio.to_thread(self.backgroundEv, form_data, ran)

    @rx.event
    def backgroundEv(self, form_data, ran) -> str:
        do = ai.Initiate(form_data, ran)
        return do.response

    @rx.event
    def on_load_data(self):
        self.height=0
        self.show_chat=False
        self.messages=[]
        self.margin="10%"
        self.margin_mobile="50%"
        self.margin_top = "70%"
        self.margin_top_tab = "30%"

    def scroll_to_bottom(self):
        return rx.call_script("document.getElementById('chat-bottom').scrollIntoView()")

    def change_messages(self, listA, indexMatch, target, change, model):
        for i, value in enumerate(listA):
          if value[indexMatch] == target:
            index = i
            break

        if index >= 0:
            listA[index] = (listA[index][0], model, change)

    def change_value(self, value: str):
        self.value = value



def qa(question: str, model: str, answer: str) -> rx.Component:
    return rx.fragment(
        rx.box(rx.text(question), text_align="right", width="100%"),
        rx.box(
            rx.cond(
            model != "DeepSeek",
            rx.badge(model, variant="outline", color_scheme="mint"),
            rx.badge(model, variant="outline"),

            ),
            rx.cond(
                answer != "Thinking...",
                rx.card(
                    rx.markdown(answer, text_align="left"),
                    surface="classic",
                    has_background=False,
                    padding="1em",
                    margin="1em"
                ),
                rx.box(
                    rx.button(
                        "Thinking", rx.spinner(loading=True), disabled=True
                    ),
                    margin="1em"
                )
            ),
            width="500px"
        ),
        margin_y="1em",
        name=State.i,
        width="100%"
    )

def qaMob(question: str, model: str, answer: str) -> rx.Component:
    return rx.fragment(
        rx.box(rx.text(question, max_width="300px"), text_align="right", width="100%"),
        rx.box(
            rx.cond(
            model != "DeepSeek",
            rx.badge(model, variant="outline", color_scheme="mint"),
            rx.badge(model, variant="outline"),

            ),
            rx.cond(
                answer != "Thinking...",
                rx.card(
                    rx.markdown(answer, text_align="left"),
                    surface="classic",
                    has_background=False,
                    padding="1em",
                    margin="1em"
                ),
                rx.box(
                    rx.button(
                        "Thinking", rx.spinner(loading=True), disabled=True
                    ),
                    margin="1em"
                )
            ),
            width="300px"
        ),
        margin_y="1em",
        name=State.i,
        width="100%"
    )

def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.messages,
            lambda messages: qa(messages[0], messages[1], messages[2]),
        ),
        width="100%"
    )

def chatMob() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.messages,
            lambda messages: qaMob(messages[0], messages[1], messages[2]),
        ),
        width="100%"
    )

@rx.page(on_load=State.on_load_data())


def index() -> rx.Component:
    return rx.container(
        rx.desktop_only(
                rx.center(
                    rx.hstack(
                        rx.button(
                            "Save", rx.badge("Soon", color_scheme="mint"), font_weight="bold", disabled=True, variant="ghost", padding="20px",
                        ),
                        justify="end",
                        spacing="5",
                        
                        font_weight="bold"
                    ),
                    rx.hstack(
                        rx.image(
                            src="/favicon.ico",
                            width="2em",
                            height="auto",
                            border_radius="25%",                    
                        ),
                        rx.heading(
                            State.title, size="8", weight="bold"
                        ),
                        align_items="center",
                        padding="20px"
                    ),
                    rx.hstack(
                        rx.link("About", href="/aboutpage", font_weight="bold", variant="ghost", padding="20px"),
                        justify="end",
                        spacing="5",
                        font_weight="bold"
                    ),
                    padding="20px",
                    justify="between",
                    align_items="center",
            ),
            rx.center(
                rx.vstack(
                    rx.center(
                        width="100%",
                        padding="5%"
                    ),
                    rx.center(
                        rx.scroll_area(
                            rx.center(
                                chat(),
                            ),
                            scrollbars="vertical",
                            style={"max-height": State.height},
                            width="100%",
                            padding="5%",
                            type="auto",
                            visible=State.show_chat
                        ),
                        width="100%"
                    ),
                    rx.center(
                        rx.card(
                            rx.form(
                                rx.vstack(
                                    rx.center(
                                        rx.select.root(
                                            rx.select.trigger(placeholder="Select Type"),
                                            rx.select.content(
                                                rx.select.group(
                                                    rx.select.item(
                                                        rx.hstack(
                                                            rx.image(
                                                                src="/favicon.ico",
                                                                width="1.5em",
                                                                height="auto",
                                                                border_radius="25%",                    
                                                            )
                                                        ),
                                                        value="Gethonis"
                                                    ),
                                                    rx.select.item(
                                                        rx.hstack(
                                                            rx.icon("sparkle", size=15),
                                                            rx.badge("Soon", color_scheme="mint")
                                                        ),
                                                        value="OpenAI",
                                                        disabled=True
                                                    ),
                                                    rx.select.item(
                                                        rx.hstack(
                                                            rx.icon("sparkles", size=15, color_scheme="tomato"),
                                                            rx.badge("Soon", color_scheme="mint")
                                                        ),
                                                        value="DeepSeek",
                                                        disabled=True
                                                    ),
                                                )
                                            ),
                                            name="Type",
                                            value=State.value,
                                            on_change=State.change_value,
                                            size="3",
                                            variant="ghost",
                                            style={
                                                "outline": "none",
                                                "border_radius": "full"
                                            }
                                        ),
                                        rx.input(
                                            outline="none",
                                            color="white",
                                            size="3",
                                            variant="soft",
                                            placeholder="Type here and wait for the magic...",
                                            background="none",
                                            border="0px solid white",
                                            panel_background="transparent",
                                            radius="full",
                                            width="90%",
                                            name="Message",
                                        ),
                                        rx.button(rx.icon("send-horizontal", size=26, variant="ghost"), type="submit", variant="ghost", color_scheme="gray"),
                                        width="100%",
                                        spacing="5",
                                    ),
                                ),
                                on_submit=State.handle_submit,
                                reset_on_submit=True,
                            ),
                            variant="classic",
                            padding="1em",
                            padding_left="2em",
                            padding_right="2em",
                            width="100%"
                        ),
                        width="100%",
                        spacing="5"

                    ),
                    width="100%",
                    margin_top=State.margin
                )
            )   
        ),
        rx.mobile_only(
            rx.center(
                    rx.hstack(
                        rx.button(
                            "Save", rx.badge("Soon", color_scheme="mint"), font_weight="bold", disabled=True, variant="ghost", padding="20px",
                        ),
                        justify="end",
                        spacing="5",
                        
                        font_weight="bold"
                    ),
                    rx.hstack(
                        rx.image(
                            src="/favicon.ico",
                            width="2em",
                            height="auto",
                            border_radius="25%",                    
                        ),
                        rx.heading(
                            State.title, size="7", weight="bold", text_align="center"
                        ),
                        align_items="center",
                        padding_top="20px",
                        padding_bottom="20px"
                    ),
                    rx.hstack(
                            rx.link("About", href="/aboutpage", font_weight="bold", variant="ghost", padding="20px"),
                        justify="end",
                        spacing="5",
                        font_size="15px",
                        font_weight="bold"
                    ),
                    justify="between",
                    align_items="center",
            ),
            rx.center(
                rx.vstack(
                    rx.center(
                        rx.scroll_area(
                            rx.center(
                                chatMob(),
                            ),
                            scrollbars="vertical",
                            style={"max-height": State.height,
                                "scrollbar-width": "none",  # Firefox
                                "-ms-overflow-style": "none",  # IE and Edge
                                "&::-webkit-scrollbar": {"display": "none"}},
                            padding="1em",
                            width="100%",
                            padding_top="1%",
                            type="auto",
                            visible=State.show_chat,
                        ),
                        width="100%"
                    ),
                    rx.center(
                        rx.card(
                            rx.form(
                                rx.vstack(
                                    rx.center(
    
                                        rx.select.root(
                                            rx.select.trigger(placeholder="Select Type"),
                                            rx.select.content(
                                                rx.select.group(
                                                    rx.select.item(
                                                        rx.hstack(
                                                            rx.image(
                                                                src="/favicon.ico",
                                                                width="1.5em",
                                                                height="auto",
                                                                border_radius="25%",                    
                                                            )
                                                        ),
                                                        value="Gethonis"
                                                    ),
                                                    rx.select.item(
                                                        rx.hstack(
                                                            rx.icon("sparkle", size=15),
                                                            rx.badge("Soon", color_scheme="mint")
                                                        ),
                                                        value="OpenAI",
                                                        disabled=True
                                                    ),
                                                    rx.select.item(
                                                        rx.hstack(
                                                            rx.icon("sparkles", size=15, color_scheme="tomato"),
                                                            rx.badge("Soon", color_scheme="mint")
                                                        ),
                                                        value="DeepSeek",
                                                        disabled=True
                                                    ),
                                                )
                                            ),
                                            value=State.value,
                                            on_change=State.change_value,
                                            size="3",
                                            variant="ghost",
                                            name="Type",
                                            style={
                                                "outline": "none",
                                                "border_radius": "full"
                                            }
                                        ),
                                        rx.input(
                                            outline="none",
                                            color="white",
                                            size="3",
                                            variant="soft",
                                            placeholder="Type here and wait for the magic...",
                                            background="none",
                                            border="0px solid white",
                                            panel_background="transparent",
                                            radius="full",
                                            width="90%",
                                            name="Message",
                                        ),
                                        rx.button(rx.icon("send-horizontal", size=26, variant="ghost"), type="submit", variant="ghost", color_scheme="gray"),
                                        width="100%",
                                        spacing="2",
                                    ),
                                ),
                                on_submit=State.handle_submit,
                                reset_on_submit=True,
                            ),
                            variant="classic",
                            padding="1em",
                            padding_left="1em",
                            padding_right="2em",
                            width="100%"
                        ),
                        width="100%",
                        spacing="5"

                    ),
                    width="100%",
                )
            ),
            margin_top=State.margin_top
        ),
        rx.tablet_only(
            rx.center(
                    rx.hstack(
                        rx.button(
                            "Save", rx.badge("Soon", color_scheme="mint"), font_weight="bold", disabled=True, variant="ghost", padding="20px",
                        ),
                        justify="end",
                        spacing="5",
                        
                        font_weight="bold"
                    ),
                    rx.hstack(
                        rx.image(
                            src="/favicon.ico",
                            width="2em",
                            height="auto",
                            border_radius="25%",                    
                        ),
                        rx.heading(
                            State.title, size="8", weight="bold", text_align="center"
                        ),
                        align_items="center",
                        padding_top="20px",
                        padding_bottom="20px"
                    ),
                    rx.hstack(
                            rx.link("About", href="/aboutpage", font_weight="bold", variant="ghost", padding="20px"),
                        justify="end",
                        spacing="5",
                        
                        font_weight="bold"
                    ),
                    justify="between",
                    align_items="center",
            ),
            rx.center(
                rx.vstack(
                    rx.center(
                        rx.scroll_area(
                            rx.center(
                                chat(),
                            ),
                            scrollbars="vertical",
                            style={"max-height": State.height,
                                "scrollbar-width": "none",  # Firefox
                                "-ms-overflow-style": "none",  # IE and Edge
                                "&::-webkit-scrollbar": {"display": "none"}},
                            padding="1em",
                            width="100%",
                            padding_top="1%",
                            type="auto",
                            visible=State.show_chat,
                        ),
                        width="100%"
                    ),
                    rx.center(
                        rx.card(
                            rx.form(
                                rx.vstack(
                                    rx.center(
    
                                        rx.select.root(
                                            rx.select.trigger(placeholder="Select Type"),
                                            rx.select.content(
                                                rx.select.group(
                                                    rx.select.item(
                                                        rx.hstack(
                                                            rx.image(
                                                                src="/favicon.ico",
                                                                width="1.5em",
                                                                height="auto",
                                                                border_radius="25%",                    
                                                            )
                                                        ),
                                                        value="Gethonis"
                                                    ),
                                                    rx.select.item(
                                                        rx.hstack(
                                                            rx.icon("sparkle", size=15),
                                                            rx.badge("Soon", color_scheme="mint")
                                                        ),
                                                        value="OpenAI",
                                                        disabled=True
                                                    ),
                                                    rx.select.item(
                                                        rx.hstack(
                                                            rx.icon("sparkles", size=15, color_scheme="tomato"),
                                                            rx.badge("Soon", color_scheme="mint")
                                                        ),
                                                        value="DeepSeek",
                                                        disabled=True
                                                    ),
                                                )
                                            ),
                                            value=State.value,
                                            on_change=State.change_value,
                                            size="3",
                                            variant="ghost",
                                            name="Type",
                                            style={
                                                "outline": "none",
                                                "border_radius": "full"
                                            }
                                        ),
                                        rx.input(
                                            outline="none",
                                            color="white",
                                            size="3",
                                            variant="soft",
                                            placeholder="Type here and wait for the magic...",
                                            background="none",
                                            border="0px solid white",
                                            panel_background="transparent",
                                            radius="full",
                                            width="90%",
                                            name="Message",
                                        ),
                                        rx.button(rx.icon("send-horizontal", size=26, variant="ghost"), type="submit", variant="ghost", color_scheme="gray"),
                                        width="100%",
                                        spacing="2",
                                    ),
                                ),
                                on_submit=State.handle_submit,
                                reset_on_submit=True,
                            ),
                            variant="classic",
                            padding="1em",
                            padding_left="1em",
                            padding_right="2em",
                            width="100%"
                        ),
                        width="100%",
                        spacing="5"

                    ),
                    width="100%",
                )
            ),
            margin_top=State.margin_top_tab
        )
        
    )


app = rx.App()
app.add_page(index)
app.add_page(about.aboutpage)
