# prio butler

Too many task at once and don’t know what to focus on first? Alfred, your own personal butler has come to help organizing your priorities.

prio butler’s process of prioritizing tasks is based on a popular matrix used by many companies and product teams around the world. By asking you just a couple of questions, Alfred will recommend which tasks you should prioritize more and which ones you might want to work on at a later point in time.

[Link to prio butler](https://prio-butler-9c7d25e6030a.herokuapp.com/)

![preview of program](assets/images/program-preview.jpg)

## Product Decisions

### User Needs

As a user I want to...

- have an overview of all of my tasks so that I don’t have to be worried to forget them
- have my tasks well-prioritized so that I know exactly which ones to focus on first
- have my list of priorities in digital form so that I can easily access them while I’m working
- be guided through the task prioritization process so that I don’t waste my time unnecessarily

### MVP

prio butler’s core functionalities focus on making sure that the most important user problems are addressed first. The user has the option to create a new task, show a list of all open tasks and their priorities, delete a task and quit the program.

### The Eisenhower Matrix

As mentioned in the introduction, the prioritization of the tasks is based on a popular matrix used by companies and product teams - The Eisenhower Matrix. Each of the tasks the user submits is evaluated based on two important criteria: importance and urgency. When the user requests to see all the tasks, they are returned as a prioritized list.

![preview of the Eisenhower Matrix](assets/images/eisenhower-matrix.jpg)

## Design Decisions

### Preparation

Before starting to code it was important to prepare a rough flow of the program to ensure that there are no unexpected obstacles and the user journey flows smoothly.

![wireframe of the program](assets/images/low-fi.jpg)

[Link to the wireframe](https://github.com/dev-timm/prio-butler/tree/main/assets/images/wireframe)


### Usability

As the UI is very limited due to the fact the the program runs in the terminal, the focus of the design lies purely on the usability.

#### Layout

To achieve an easy and effortless overview of the interface, there are line spaces added intentionally between sections. This helps the user to digest larger amounts of text information better and therefore increases the overall user experience.

#### Colors

To further improve the usability of the program, user’s input is displayed in a light green color. This enables the user to quickly scan through their own inputs.

#### Interaction Style

To bring more life into the application, prio butler was designed in a way that the users feel like they interact with another human. “Alfred”, the personal butler, leads the users through the application until they decide to close it. Therefore, it is intended that the user enters short words to navigate through the app instead, for example, numbers in front of the options.

## Features

### Welcome Message

When starting the program users are welcomed by Alfred who then asks for their name. Depending on whether the user is a new one or a returning one, they will be redirected to a different flow. New users will be prompted to create their first task, while returning users will be redirected to the main menu.

![Welcome message](assets/images/welcome-message.jpg)

### Menu

The menu gives users a choice between four different actions: create a task, show all tasks, delete a task and quit the program.

![Program menu](assets/images/menu.jpg)

### Create a New Task

The user can create a new task by it giving a title and deciding whether the task is important and/or urgent.

![Create new task](assets/images/create-new-task.jpg)

### Show List of Tasks

The user can see all added tasks in one list. The list is structured into different sections depending on how the user evaluated them based on the questions regarding importance and urgency.

![List of all tasks](assets/images/list-of-tasks.jpg)

### Delete a Task

Any task that was created can also be deleted by the user. This feature displays a list of all tasks and by typing the number to its left, the task will be deleted.

![Delete task](assets/images/delete-task.jpg)

### Goodbye Message

When the user decides to quit the program, a goodbye message will be displayed.

![Goodbye Task](assets/images/goodbye-message.jpg)