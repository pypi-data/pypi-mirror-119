# Mandatum
Mandatum is a python framework based on rich-python to create beatiful Command-Line-Interface applications in no time. It can create interface for your application in an object oriented approach

## Installation
To install via pip type the following command
```bash
pip install mandatum
```

OR

Install poetry
```bash
pip install poetry
```

Clone this repo
```bash
git clone https://github.com/ZayedMalick/mandatum
```

Change directory to mandatum and type
```bash
poetry install
```

## Getting Started
Lets create a basic application with mandatum

```python
import mandatum

# display
display = mandatum.Display()

# print
display.print(text="Hello World!", style="bold red", justify="center")

```

The above application was a very simple one , now lets make a bit complicated application
```python
import mandatum

# Initial setup
menu = mandatum.Menu(options=["Opt1", "Opt2"], bold_text=True)
prompt = mandatum.Prompt(color="blue")
alert = mandatum.Alert(bold_text=True)
warning = mandatum.Warning()
display = mandatum.Display()


if __name__ == "__main__":

    # Displaying Menu
    menu.start()

    # User name
    name = prompt.input("\nEnter your name : ")
    display.print(text=name, style="bold green", justify="left")

    # Alerts
    alert.alert("\nAlerting")

    # Warning
    warning.warn(message="\nWarning!", bold_text=True)
```

## Projects made with mandatum
- [CalculusQR-CLI](https://github.com/ZayedMalick/CalculusQR-CLI)

## License
mandatum is licensed under the terms of MIT license

## Important Note
Version 2.0.0 is coming soon and will contain major syntax and performance change. 
