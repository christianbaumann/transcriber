# Slide 1: Don’t be a fool
with a tool

Fundamental knowledge for
proper test automation
Christian Baumann
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Hello and welcome to my talk 

Don’t be a fool with a tool
Fundamental knowledge for proper test automation

Thanks everybody for joining,
and a special thank you to the nice ask-UI people, 
for inviting me.

---

# Slide 2: Who is that guy?

**Christian Baumann** Software Tester
**@chrissbaumann     @chrissbaumann@sw-development-is.social**

### Notes
My name is Christian Baumann, and I’m a software tester at MaibornWolff.
In my free time 
- I like spending time with my family, reading fantasy books, 
- riding my motorbike, learn about testing & coding, 
- and I also play the clarinet and the saxophone in a band.
- And Lego even made a minifigure out of me.
For more info about me, you can check out my Twitter and Mastoton, there’s a link to my different profiles in my bio.

---

# Slide 3: Does working on your test automation feel like this?

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Let me explain you, what this talk about.

Many people get into test automation without having a profound back-
ground in programming or without receiving any proper training.
They have some idea about what tool to use, gathered some basic knowledge and managed to create some automated tests with it.
At a certain point they suspect, that  something is not quite right with their automation.
The code feels messy and maintaining it is hell, costs a lot of time and is very frustrating..

Don’t worry, this talk has you covered! - I’ll talk about
Test automation strategy
Test data management
Object oriented programming principles, 
Code smells,
The idea of Clean Code, and
Design Patterns in Test Automation

Basically, I’ll cover the things I wished I had known more than 15 years ago, when my test automation journey began...
Each of these topics is huge, so this talk cannot cover them all in detail, but it is intended to give you some hints and starting points for further studies and research.

---

# Slide 4: How not to start

*Weeks of coding can save you hours of planning.*
Unknown
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Way too often, people immediately jump into coding their 
test automation, without having a strategy or plan at hand. 

Usually this leads to a lot of problems 

---

# Slide 5: Strategy vs Plan ?

BBST:
- Strategy
- Logistics
- Plan
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
So what about a test strategy or a test plan, or maybe both?

But what’s the difference between a test strategy and a test plan? 
Or are they just different words for the same thing?

According to the Black Box Software Testing definition by Kaner and Bach,
a test strategy answers the question: “Given a testing mission, how will you achieve it?”

Where they define
Strategy - as the set of ideas that guide your test design
Logistics - as the set of ideas that guide your application of resources, and
Plan - as the combination of your strategy, your logistics and you project risk management

Having a strategy and/ or plan in place for your test automation,
helps to eliminate a lot of unclarity, and guides you throughout the project, and thus reduces the chance of failure.

---

# Slide 6: Ask questions

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Asking questions helps you to formulate your 
strategy and plan:

What is the goal for the test automation and what shall be accomplished?
What should be tested?
Who should do the the automation and in what capacity?
How to plan for the execution of the strategy?
How to test?
When to test?
Where to test?

---

# Slide 7: Models

**Test Automation Pyramid**
**Automation Wheel**
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Also models can be of great help, when formulating a test automation strategy, or a test strategy in general.

According to Michael Bolton, 
Good models are a set of guidelines to help us solve a problem.

This is also true for test automation. 
Common models used to guide your test automation are the test automation pyramid and the automation wheel.
There are more, like the software testing ice cream cone or the agile testing quadrants.

But please keep in mind, that models are not reality - “All models are wrong, some are useful.”

---

# Slide 8: Test Data Management

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Let’s talk about test data, 
or test data management.

And the differences in test data management 
when automating your tests,
and when testing manually.

---

# Slide 9: Test Data on the fly

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
When testing manually, in most cases,
the test data is entered by the tester on the fly.

Mostly, shortly before or even during the test execution.
Either the tester knows, which data is required to execute a test, 
or it’s mentioned as a precondition in the documentation of the test.

This “on the fly” approach is not feasible for automated tests.

---

# Slide 10: Test Data needs to be under control

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Automated tests rely on certain data,
that they require as precondition for successful execution.

Imagine, using a shared test environment, 
and the automated tests assume, a certain set of data to be available in the system.
In case someone modified or deleted that data, the automated tests will fail.

Who has experienced this before?
Please show me your hands!

I think we all agree, that this is a no-go, and thus, for automated tests, you need have the test data under control.

---

# Slide 11: Test Data strategies

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
I am simplifying here, but in general there are two 
commonly used approaches, 
to ensure your automated tests have the 
data available they rely on:

Approach 1
You ensure that all data for all tests is available in the system upfront. 
Either on database level, eg. by loading a certain backup, or by running a script prior to the test execution, that inserts all necessary data into the system.

Approach 2
Each test creates its very own data, as part of its test setup.
Also: After the test execution, all created data should be deleted again, to not pollute the system under test.

Which strategy of managing test data you choose, depends on your project and environment.

---

# Slide 12: OOP Principles

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Next, let’s talk about the four basic principles of
object oriented programming: 

Encapsulation, 
Abstraction,
Inheritance and 
Polymorphism.

Let’s have a closer look at each of them.

---

# Slide 13: Encapsulation

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Say we have a program. 

It has a few logically different objects which communicate with each other - according to the rules defined by the program.
Encapsulation is achieved when each object keeps its state private, inside a class. 

Other objects don’t have direct access to this state. Instead, they can only call a list of public functions — called methods.
So, the object manages its own state via methods — and no other class can touch it, unless explicitly allowed.

If you want to communicate with the object, you should use the methods provided. But by default, you can’t change the state.

---

# Slide 14: Abstraction

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Abstraction can be seen as a natural extension of encapsulation.

In object-oriented design, programs are often pretty large. 
And separate objects communicate with each other a lot. 
So maintaining a large codebase like this for years — with changes along the way — is difficult.

Abstraction is a concept aiming to ease this problem.
Applying abstraction means that each object should only expose a high-level mechanism for using it.
This mechanism should hide internal implementation details, it should only reveal operations relevant for the other objects.

---

# Slide 15: Abstraction

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
You see, other people, not working in IT, 
have recognized the concept of abstraction as well…

---

# Slide 16: Inheritance

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
In object oriented programming, objects are often very similar. 
They share common logic. 
But they’re not entirely the same.

So how do we reuse the common logic and extract the unique logic into a separate class? 
One way to achieve this is inheritance.

It means that you create a child class, by deriving from another parent class. This way, you form a hierarchy.

The child class reuses all fields and methods of the parent class (the common part), and can additionally implement its own unique part.

---

# Slide 17: Polymorphism

**Figure Interface**
Whoever uses it,
must implement:
- calculateSurface()
- calculatePerimeter()
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
So we already know the power of inheritance, but there is a potential
problem.
Let’s say we have a parent class and a few child classes which inherit from it. 
Sometimes we want to use a collection — for example a list — which contains a mix of all these classes. 

This can be solved by using polymorphism.
Simply put, polymorphism gives a way to use a class exactly like its parent so there’s no confusion with mixing types. 
But each child class keeps its own methods as they are.
This typically happens by defining a (parent) interface to be reused.
The interface outlines a bunch of common methods. Then, each child class implements its own version of these methods.

Any time a collection or a method expects an instance of the parent - where common methods are outlined,
the language takes care of evaluating the right implementation of the common method — regardless of which child is passed.

---

# Slide 18: OOP Principles

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
So, on a really high level, we can say:

Encapsulation means “hide the data”,
Abstraction “provides templates to be implemented”,
Inheritance can be shortened to “extend data and behaviour”, and
Polymorphism is “the ability to take multiple forms”.

Applying those principles in your test automation code will be of great help and make your life much easier, by making your code easier to read, understand and maintain.

Angie Jones has a great talk with examples on how to apply OOP principles in test automation, 
a link to that talk can be found in the resource section of the slides.

---

# Slide 19: Code smells

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Let’s talk about code smells.
Well, actually not this kind of smell...

---

# Slide 20: Code smells

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
...but more like this.
But what are “code smells”?

One way to look at smells is with respect to principles and quality.

---

# Slide 21: Code smells

*Smells are certain structures in the code that indicate violation of fundamental design principles and negatively impact design quality.*
Suryanarayana, Samarthyam, Sharma
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Smells are certain structures in the code
that indicate violation of fundamental design principles 
and negatively impact design quality.

Code smells are usually not bugs; they are not technically incorrect and do not prevent the program from functioning.
Instead, they indicate weaknesses in design that may slow down development or increase the risk of bugs or failures in the future.
Bad code smells can be an indicator of factors that contribute to technical debt.

---

# Slide 22: Long class

- no single responsibility
- hard to find things
- difficult to maintain
- hard to unit test
- does not “fit in my head”
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Let’s talk about a code smell example: The long class

The class at the right has nearly 500 lines, and it probably isn’t the longest class that exists, still it causes some problems:

- there is no single responsibility, instead it is taking too much responsibility
- It is hard to find things
- It is difficult to maintain
- there is a lot of private nested code, which is hard to unit-test, because it has 
       no public interface.
- it does not “fit in my head”

Martin Fowler, who provided this real world example, says about this class:

It's bloated and convoluted and impossible to fit in my head. This has 
created a nasty feedback loop: "Because this code is so hard to reason about, refactoring will take more time and energy than I have, so I'll put up with it even longer - even though it means I can't even make small changes any more because it takes so long for me to understand the code's current state and decide where the change should go."

---

# Slide 23: Too many arguments

- low maintainability
- low reuse
- coupling
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Another code smell is “too many arguments”, this means objects or 
methods need too many arguments to work.

Problems that too many arguments cause, are 
- low maintainability and 
- re-use, and 
- coupling.

---

# Slide 24: Too many arguments

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
This is an example of “too many arguments”.
But how to solve this?

---

# Slide 25

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
This is one possible solution.

In order to achieve it, you should relate arguments and group them

You should favor real world mappings. 
That means, how to group them in real world matches how to group the arguments in cohesive objects.

If a function gets too many arguments, some of them might be related to the class construction, which is a design smell too.

---

# Slide 26: Tight coupling

- two objects are dependent on each other’s data and/or functions
- changing code becomes a nightmare
- likely to introduce bugs
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Since “coupling” is a potential side effect of the “too many arguments” smell,
let’s talk about coupling next.

Tight coupling is when two objects are so dependent on one another's data and/or 
functions, that modifying one requires modifying the other. 
When two objects are too tightly coupled, making changes to code can be a 
nightmare and you're more likely to introduce bugs with every change.

---

# Slide 27: Tight coupling

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
In this case, Worker and Bike are tightly coupled.
What if one day you wanted to drive a Car instead of a Bike for your commute? 
You'd have to go into the Worker class and replace all Bike-related code with Car-related code.
It's messy and prone to errors.

---

# Slide 28

**@chrissbaumann @chrissbaumann@sw-development-is.social**

### Notes
You can loosen coupling by adding a layer of abstraction. 
In this case, the Worker class doesn't just want to drive Bikes, but also Cars, and maybe Trucks, possibly even Scooters.
These are all Vehicles, aren't they? 
So create a Vehicle interface, which allows you to insert and replace different Vehicle types as desired.

By the way, I promised you another example for Polymorphism earlier, 
when talking about the basic principles of object oriented programming. Here it is...

---

# Slide 29: Duplicate code

- perform the same logic in multiple areas
- likely to introduce bugs when changing
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Duplicate code means, you perform the exact same logic in multiple 
unrelated areas of your program.
Later, you realize you need to modify that logic, but don't remember all 
the places where you implemented it.
You end up changing it in only 5 out of 8 places, resulting in buggy and 
inconsistent behaviors.
Duplicate code is a prime candidate for being turned into a function.

---

# Slide 30: Duplicate code

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
For example, let's say you're developing a chat application and you write this…

Somewhere else in the code, you realize you need to perform the very same "is this user online?" check.

Instead of copy-pasting the loop...you can pull it out into a function…

---

# Slide 31: Duplicate code

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Now anywhere in your code, you can use the isUserOnline() check.

If you ever need to modify this logic, you can tweak the method and it'll apply everywhere it's called.

---

# Slide 32: Switch statements

- switch statements with a type code
- bear the risk of duplicated code
- anti-pattern open closed principle
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
One of the symptoms of object-oriented programming is to use 
switch statements (or a cascade of if-else-statements) with a
type code to get different behavior

Switch statements bear the risk of duplicated code, 
and they are an anti-pattern to the open-closed principle, 
which states that entities should be open for extension, but closed for modification.

---

# Slide 33: Switch statements

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Imagine that we have some client class that calculates the area and perimeter of particular geometrical figures.

This code is clearly a poor design that limits the current client to only work with three types of figures.
There are usually several places in the code where the behaviour slightly deviates 
and these switch statements are present (e.g. in calculateSurface and calculatePerimeter methods).

It’s even worse if we work with objects where the switch is replaced by multiple instance of if-conditions.

---

# Slide 34

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
To improve the design you can make Square, Rectangle and Circle 
have a common root. Meaning, that they either extend the same class, such as AbstractFigure or that they implement a common interface, such as Figure.

Then you can eliminate the switch statement code smell very easily. 
You replace it with polymorphism.

And such refactoring simplifies the Client code.
It also allows for easy extensibility by implementations of other figures without changing a single line of Client code.

Another way of looking at it, is from the responsibility point of view:
Why should the client be responsible for calculating the area or the perimeter; or have a knowledge about a figure’s internals (e.g. number of sides, radius, etc.)
This is the responsibility of each figure, and all that the client needs to know is that a figure has a perimeter and area.

So using polymorphism not only helps to avoid coupling, but also can overcome the switch statement code smell.

---

# Slide 35

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Other types of code smells are

Not communicating the intend
Or comments explaining hard to read or hard to understand code
And plenty more…

Code smells can be avoided by applying object oriented programming principles as well as Clean Code principles

---

# Slide 36: Clean Code

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Clean…. What? - you might say

Code is clean if it can be understood easily – by everyone on the team.
Clean code can be read and enhanced by a developer other than its original author. 
With understandability comes
readability, 
changeability, 
extensibility and 
maintainability.

Clean Code consists of rules and principles to follow, in order to achieve clean code, without smells.

---

# Slide 37: Clean Code

*Always code as if the guy who will ultimately maintain your code will be a brutal psychopath who knows where you live.*
Martin Golding
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Martin Golding's famous quote is:

Always code as if the guy who will ultimately maintain your code
will be a brutal psychopath who knows where you live.

Writing clean code makes it easier to understand the code 
and is necessary to create successful test automation code, that you can maintain.

Programmers are authors, and your target group is not a computer; 
these are other programmers (and you).

---

# Slide 38: Clean Code

*Any fool can write computer-understandable code. Good programmers write code that people can understand.*
Martin Fowler
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
To quote Martin Fowler: 

Any fool can write computer-understandable code. 
Good programmers write code that people can understand.

To be able to write clean code, you should train your mind for some time. 
The hardest part is just the beginning; but as time goes on, the skill set gets better.
Writing clean code is readability, so even the smallest things, such as changing your naming habits, make the biggest difference.

---

# Slide 39: Clean Code

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Let’s do a quick check on the concept of readability.

Both code fragments do exactly the same.

Which one do you think is “better” in terms of clean code.

…

It’s clearly the second one.
It’s a bit longer, but it can be easily understood and read like natural language.

---

# Slide 40: Clean Code - General Rules

- Follow standard conventions
- Meaningful names
- KISS - Keep it simple, stupid!
- Boy scout rule
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
According to the clean code idea, 
there are some general rules to follow:

Follow standard conventions.
Meaningful names
KISS - Keep it simple stupid. 
The boy scout rule
And many more...

Let’s have a closer look at some of them

---

# Slide 41: Follow standard conventions

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Let me quote the “Clean Code” book on following standard 
conventions:

Every team should follow a coding standard based on common industry norms.
This coding standard should specify things like where to declare instance variables;
how to name classes, methods, and variables; where to put braces; and so on.
The team should not need a document to describe these conventions because their code provides examples.

Everyone on the team should follow these conventions.
This means that each team member must be mature enough to realize 
that it doesn’t matter a white where you put your braces, 
so long as you all agree on where to put them.

---

# Slide 42: Meaningful names

- Intention-Revealing names
- Pronounceable names
- Class names
- Don’t be cute
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Names are everywhere in software. We name our variables, our functions,
our arguments, classes, and packages. 
We name our source files and the directories that contain them. 
We name our jar files and war files.
We name and name and name. Because we do so much of it, we’d better do it well.

I will only present a few rules for naming, you can find more of these in the resource section of the slides

- Use Intention-Revealing Names
It is easy to say that names should reveal intent. 
Choosing good names takes time but saves more than it takes. 
So take care with your names and change them when you find better ones. 
Everyone who reads your code (including you) will be happier if you do.

- Use Pronounceable Names
If you can’t pronounce it, you can’t discuss it without sounding like an idiot. 
“Well, over here on the B-C-R-3-C-N-T we have a P-S-C-K-Y integer, see?” 
This matters because programming is a social activity.

- Class Names
Classes and objects should have noun or noun phrase names like Customer, WikiPage, Account, or AddressParser. 
Avoid words like Manager, Processor, Data, or Info in the name of a class. 
Also, a class name should not be a verb.

- Don’t Be Cute
Will they know what the function named Holy-Hand-Grenade is supposed to do? 
Sure, it’s cute, but maybe in this case Delete-Items might be a better name. 
Choose clarity over entertainment value. Say what you mean. Mean what you say.

---

# Slide 43: KISS - Keep it simple, stupid!

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
KISS: Keep It Simple Stupid. 

A design principle originating from the U.S. Navy that goes back to 1960s already.
It states that most systems should be kept as simple as possible.
Unnecessary complexity should be avoided.
The question to ask when you're writing code is "can this be written in a simpler way?"

Simple code is less prone to bugs, and is easier to read and understand for you
and the people who'll be working on the code in the future (including yourself)

Keeping things simple is, ironically, not simple!
It requires abstract thinking. It requires knowledge of the domain you're working on. 
It requires knowledge of the code, the framework, and the language you're working with.
And it also requires experience.

---

# Slide 44: Scout rule

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Next rule to discuss, is the scout rule, which says:

Always leave the campground cleaner than you found it
When you find a mess on the ground, clean it, doesn’t matter who did it.
Your job is to always leave the ground cleaner for the next campers.

For programming, this can be expressed as
Always leave the code cleaner than you found it.

Meaning that every time that we make a change in our code base, make an improvement in the code.

There are many ways to apply the boy scout rule to your code, it doesn’t have to be something big:
You can rename a variable to a more meaningful name, get rid of a small duplication or break up a long function..

---

# Slide 45

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
There are some more principles & rules to follow, such as

DRY - Don’t repeat yourself
SOLID principles
The source code structure

and many more.

Next topic, I want to talk about, is design patterns.
Florian’s talk yesterday already was about design patterns,
still let’s revisit some of them.

---

# Slide 46: Design patterns

*A design pattern is a general, reusable solution to a commonly occurring problem within a given context in software design.*
Wikipedia
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
A design pattern is a general, reusable solution to a commonly occurring 
	problem within a given context in software design.

Design patterns can speed up the development process by providing tested, proven development paradigms.

They also help to prevent hidden subtle issues that often are detected only late in the process.

Furthermore they  also improve code readability for coders and architects who are familiar with the patterns.

---

# Slide 47: Page Object Model

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
Maybe the best known design pattern in test automation is the 
page object model, or in short POM.
It models the application under test, 
thus keeps the tests independent from the implementation details of the software under test
and reduces maintenance efforts when the application changes.

---

# Slide 48: Screenplay Pattern

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
The screenplay fulfills a similar purpose.

It aims at writing tests like screenplays,
by structuring complex test code in a way that makes it more
readable,
reusable, and
maintainable.

It does that, by taking a user-centric and object-oriented view on things.

In screenplay, a user is represented as an Actor. 
Actors can have Abilities. 
Abilities enable them to do Tasks or answer Questions.

In screenplay each of these concepts 
—​Actor, Ability, Task and Question—​ 
are objects which abstract from the actual actions.

---

# Slide 49: Object Mother Pattern

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
The ObjectMother pattern is used for test data generation.
It starts with the factory pattern,
by delivering prefabricated test-ready objects via a simple method call. 

It moves beyond the realm of the factory by
facilitating the customization of created objects, 
providing methods to update the objects during the tests, and
if necessary, deleting the object from the database at the completion of the test.

Some reasons to use ObjectMother are
reduction of code duplication in tests, thus increasing maintainability
test objects are super-easily accessible
every test runs with fresh data, and
tests always clean up after themselves.

---

# Slide 50: Summary

**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
This was “Don’t be a fool with a tool - fundamental knowledge 
for proper test automation”, before I close the session, 
let’s quickly recap, what I presented:

First of all: Have a strategy - asking questions and using models can help to build it.

Manage your test data properly.

Following OOP & clean code principles, and using design patterns, help a lot to avoid code smells.

As said, in the duration of this talk, I could not cover the topics in detail, but that wasn’t the purpose of this talk.
The intention was, to present strategies and approaches to make your test automation successful,
and you can further study and research these topics on your own.

I will share the link to slides on Twitter and LinkedIn: at the very end, there’s a resource section, with links to articles and talks for your further learnings.

---

# Slide 51

Thank you! Questions?
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

### Notes
This was my talk, many thanks for your attention.

I hope you found some useful bits for your work.

I’m happy to answer any questions you might have
tomorrow at the “ask me anything” or just catch me during a break.

---

# Slide 52: Ressources

**Automation Strategy**
testingeducation.org/BBST/foundations/BBSTFoundationsNov2010.pdf
satisfice.com/download/rapid-software-testing-context-model
testautomationu.applitools.com/setting-a-foundation-for-successful-test-automation/chapter1.html
ministryoftesting.com/dojo/lessons/an-introduction-to-the-automation-test-wheel
martinfowler.com/articles/practical-test-pyramid.html
dzone.com/articles/your-automation-testing-strategy-pyramids-triangle
developsense.com/articles/2005-10-ElementalModels.pdf
en.wikipedia.org/wiki/All_models_are_wrong
twitter.com/codewisdom/status/1002181404061552640
**OOP principles**
angiejones.tech/oop-test-automation/
medium.com/@cancerian0684/what-are-four-basic-principles-of-object-oriented-programming-645af8b43727
freecodecamp.org/news/object-oriented-programming-concepts-21bb035f7260/
en.wikipedia.org/wiki/Object-oriented_programming
twitter.com/Ronalfinnho/status/1529048604882653186
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

---

# Slide 53: Ressources

**Code smells**
angiejones.tech/test-automation-code-smells/
informationweek.com/architecture/in-praise-of-small-code/d/d-id/1098422
en.wikipedia.org/wiki/Code_smell
openlibrary.org/books/OL28011853M/Refactoring_for_Software_Design_Smells
cs.wm.edu/~denys/pubs/ICSE'15-BadSmells-CRC.pdf
martinfowler.com/articles/class-too-large.html
makeuseof.com/tag/code-smells-fix/
en.wikipedia.org/wiki/Open%E2%80%93closed_principle
hanuska.blogspot.com/2006/08/swich-statement-code-smell-and.html
maximilianocontieri.com/code-smell-10-too-many-arguments
**Clean Code**
gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29
goodreads.com/book/show/3735293-clean-code
goodreads.com/book/show/4845.Code_Complete
prezi.com/7t48cecbnw79/agile-partner-agile-metteg-clean-code
planetgeek.ch/wp-content/uploads/2013/06/Clean-Code-V2.2.pdf
programandola.site/helpful-hints-for-writing-clean-code
moderatemisbehaviour.github.io/clean-code-smells-and-heuristics/general/g24-follow-standard-conventions.html
x-team.com/blog/principles-clean-code
simpleprogrammer.com/kiss-one-best-practice-to-rule-them-all
matheus.ro/2017/12/11/clean-code-boy-scout-rule
medium.com/@huytrongnguyen1985/lessons-learnt-from-the-clean-code-robert-c-martin-cecbe2b09139
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

---

# Slide 54: Ressources

**Design Patterns**
testautomationu.applitools.com/selenium-webdriver-tutorial-java/chapter4.1.html#we-re-going-to-use-a-pattern-called-the-page-object-model-design-pattern
angiejones.tech/page-object-model/
serenity-bdd.github.io/theserenitybook/latest/serenity-screenplay.html
shakespeareframework.org
martinfowler.com/bliki/ObjectMother.html
http://wiki.c2.com/?ObjectMother
citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.18.4710&rep=rep1&type=pdf
en.wikipedia.org/wiki/Software_design_pattern
**@chrissbaumann          @chrissbaumann@sw-development-is.social**

---

# Slide 55: Images

pexels.com/de-de/foto/arbeiten-lesen-studieren-drinnen-8086372
pexels.com/de-de/foto/borsenvorstand-210607
pexels.com/de-de/foto/braune-und-weisse-cupcakes-auf-schwarzem-tablett-3805539
pexels.com/de-de/foto/foto-von-kindern-die-ihre-mutter-kussen-4473782
pexels.com/de-de/foto/foto-von-zwei-personen-shakehands-2058130
pexels.com/de-de/foto/fragezeichen-auf-brauner-oberflache-5428835
pexels.com/de-de/foto/frau-madchen-sitzung-weiss-9486568
pexels.com/de-de/foto/frau-zeichnen-sie-eine-gluhbirne-in-white-board-3758105
pexels.com/de-de/foto/nackter-kuchen-1727415
pexels.com/de-de/foto/nahaufnahme-fotografie-der-frau-die-rosa-rose-riecht-1170654
pexels.com/de-de/foto/sitzung-boden-braun-kinder-9303753/
pexels.com/de-de/foto/vogel-fliegen-tier-gefieder-6387497
pxfuel.com/en/free-photo-embkb
pxfuel.com/en/free-photo-jlajv
pxfuel.com/en/free-photo-oqhag
pxfuel.com/en/free-photo-oxatu
pxfuel.com/en/free-photo-qffwo
wordart.com
**@chrissbaumann          @chrissbaumann@sw-development-is.social**
