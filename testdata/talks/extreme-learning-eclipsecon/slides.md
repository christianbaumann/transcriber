# Slide 1: Extreme learning situations as testers

How to add value while you're still learning
Christian Baumann
**@chrissbaumann #EclipseCon 2020**

### Notes
Hello and welcome to my talk 

Extreme learning situations as testers

How to add value while you’re still learning”

---

# Slide 2: Who is that guy?

**Christian Baumann**
Software Testing for 15+ years
**@chrissbaumann**
**\#EclipseCon**
**@chrissbaumann #EclipseCon**

### Notes
My name is Christian Baumann, and I’m a software tester.

For more about me, you can check out my Twitter,
there’s a link to my different profiles in my bio.

When tweeting about this talk, please use the hashtag #EcliseCon

So, let’s start

---

# Slide 3

**@chrissbaumann #EclipseCon**

### Notes
Let me explain you, what this talk about.

When joining a new project, or taking on a new role, it is often required to learn new skills and technologies

Be it a new business domain, a new test tool, 
a new technology the product is build with, 
a new test technique or kind of testing 
or whatever else
Also we often feel the need - or are told of the need - to provide value to the project quickly 

Both of these competing expectations are normal to a certain degree, 
and working in IT, we’re used to that - be it as testers, programmers or whatever our job title is

When I started a new job at a Fintech startup last year,
joining a project where it was my task to test an API against a European Union standard for payment services,
I had to do both to an extreme I had never experienced before

The list of things to learn from almost the ground was long…

---

# Slide 4

PSD2
**@chrissbaumann #EclipseCon**

### Notes
Let’s briefly talk about the Application Under Test

The Payment Service Directive PSD2 is an EU directive to regulate payment services throughout the European Union

Basically, banks have to have a standardized API for so called 3rd party providers,
which can be used by merchants to access end clients’ account informations and to initiate payments

The two most relevant points are
It's a REST API
The specification comes from a european institution, 
thus is relatively difficult to comprehend because of its very official language

---

# Slide 5

**@chrissbaumann #EclipseCon**

### Notes
So the main things I needed to learn were:

Testing an API
I basically knew what an API is: You send a request, and get some data back
But how to test that?
I needed to perform Exploratory Testing, in order to learn about the API and to find problems
Automate the tests using Postman.
We had promised our clients to give them a set of Postman tests,
so they would be able to perform some checks on their own, so Postman was set.
Also, for banks in Luxemburg, the financial regulator demanded performance tests being executed
Beyond being aware of the existence of some API testing tools like Postman and SoapUI, 
my knowledge about API testing was quite close zero.

I also had to learn the Specification
Which consisted of 400 pages (authored by a public institution, thus very detailed, 
overstructured & overcomplete, thus quite difficult to comprehend.)

Finally I had to learn the Business Domain
I never worked in the financial industry before, so I had to at least grasp the basics: 
What’s a consent and how does it work? 
How does a payment payment work? 
What different types of payments exist and how do they differ? 
To name just a few things to be learned within the business domain

---

# Slide 6

**@chrissbaumann #EclipseCon**

### Notes
Despite all these things to learn, other project members were expecting valuable contributions from me shortly after joining.
Luckily, nobody ever put any direct pressure on me!
Just certain things where “in the room”, plus the pressure I put myself under
But that might be different other contexts

Some expectations:
I joined April 1st, the instructed go live date for the UAT environments was June 14th. So that was roughly 2.5 months
It was expected that the system is “completely tested” (whatever completely tested means) before that date. 
Another expectation was, that I should find “all the bugs” (another very questionable statement)
The test automation should be fast forwarded
The Postman tests needed to completed to be delivered to our clients. When I joined, only skeletons existed, and only for a fraction of cases
Performance tests needed do be done before the end of April

---

# Slide 7

**@chrissbaumann #EclipseCon**

### Notes
So let me share with you some stories of my project, 

and explain the strategies, techniques and tools, I used to deal with all the competing requirements

---

# Slide 8

**@chrissbaumann #EclipseCon**

### Notes
First of all, it is important to find out about what the most important priority is, or what the most important priorities are, so that you have a starting point.
But how to do that?

First of all: Talk to the people involved in the project and to the stakeholders about what their priorities are.
Question those priorities, ask why those are priorities to them.
Often there will be misalignments between different people involved in the project and it's part as testers to spot and clarify them

Second: Bring your own judgement as tester to the table
You’re a skilled and experienced professional, and you´re totally able to get the job done,
that’s the reason you got hired or assigned. So don’t be shy, you have something to bring to the table.
Bringing your judgement to the table might change estimates, deadlines or priorities 
For example someone with little to zero knowledge might have given a totally unrealistic estimate about how much time is needed to setup and execute performance tests.
Ask questions like: What exactly shall be achieved? What is required or shall be done? What is the goal?
At least certain aspects of the project and the priorities might change because of that, and it will result in a clearer view on what is a priority.

Third point about finding out about priorities is to check deadlines and plan accordingly

This planning should be updated regularly, by re-doing the before mentioned steps, but also based on your learnings and new inputs and insights

---

# Slide 9

**@chrissbaumann #EclipseCon**

### Notes
Next I’ll talk about how I handled multiple parallel tasks throughout the project.

We all now that multitasking is far from being ideal, but sometimes it’s hard to get around it.

---

# Slide 10

**@chrissbaumann #EcliplseCon**

### Notes
Okay, if you cannot avoid multitasking, be at least aware of the negative effects it has, 
and your boss should be aware of these too

You get tired faster

You easily feel overwhelmed

You tend to make more mistakes

---

# Slide 11

**@chrissbaumann #EclipseCon**

### Notes
Most important thing to consider is: Focus!

Things that help to focus on a specific task are
Avoid task switching too often
Stay focused: Work in bigger blocks of at least two hours to avoid too much task switching
If you have too many meetings: Try to block time in your calendar for working
task switching costs up to 40% of someone´s productive time
(various studies with different numbers, but this is not about the absolute truth, but to get an idea.)
Come to the office early, or stay late (not to work over hours, but early & late the office is relatively quiet, 
and there are less people there to disturb you)
Another possibility to avoid the usual office distractions is to work from home (well, before the pandemic and the kids being homeschooled all day)

---

# Slide 12

**@chrissbaumann #EclipseCon**

### Notes
A great tool to Use is the Pomodoro technique

Pomodoro is italian and means tomato
The technique has that name because of those old fashioned kitchen timers, that often have the shape of a tomato

How does the technique work?
Basically, you work on a task in blocks of 25 minutes, followed by a 5 minutes break
Within that 25 minutes, you don’t work on anything else and avoid any distractions: No emails, no phone calls, no WhatsApp, no Facebook!
Every 4 blocks, you take a bigger break of around 20 minutes

---

# Slide 13

**@chrissbaumann #EclipseCon**

### Notes
Besides focusing, what are other ways to handle multitasking if you think you can not avoid it?

First of all: Evaluate, if you really have to multitask.
Talk to you stakeholders and your boss. 
Tell them for example
	- Do you want both of these tasks to be ready in 2 weeks? 
	- Or is it ok to focus on one at a time, deliver the first one by the end of this week, and the second task done by the end of next week? 
	- Most likely I will be done with both tasks in less than two weeks, because I’m not losing time due to task switching
Next you should evaluate if you can eliminate unnecessary things?
Or if there are things that you can supervise or delegate? 
Also check what can you simplify.
Here some other advantages of the Pomodoro technique come into play, Pomodoro helps you
learning to concentrate and to work in blocks of time (what I said earlier)
It also is a great help in avoiding procrastination and distraction
You also should make a plan & establish personal goals (For that I can recommend the book “Pomodoro Technique illustrated” by Staffan Noteberg)
Techniques like Bullet Journaling or Momentum Planners also help with that
You need to align your priorities regularly. For that you should check with the team, the stakeholders and your boss
It is also very important to accept your limits, to work at a sustainable pace and take breaks when you need them

---

# Slide 14

**@chrissbaumann #EclipseCon**

### Notes
Let’s talk about “Learning while doing”.

How does learning an instrument work? 
Do You study music theory for a couple of years and only when you master it, access an instrument for the very first time? 

Certainly not!
The instructor tells you just a tiny little bit on how to get started, you practice that, 
and with each lesson, you learn and practice a little bit more about every aspect: 
Theory & practice about how to play that instrument, and over time you become proficient.

---

# Slide 15

**@chrissbaumann #agileTD**
**@chrissbaumann #EclipseCon**

### Notes
Remember: It doesn’t have to be perfect from the beginning. 
Very often it doesn’t even need to be perfect in the end, but that’s a topic for a talk on it’s own.

I didn’t have the time to first acquire all the necessary skills, not even talking about bringing them to perfection.
I followed a similar approach as when learning an instrument.
Just studying enough to get me started. Then try to use that, and improve over time.

Let me give you an example of that:
When I arrived, in the existing postman tests, there was a gap: You had to copy a URL l from Postman, 
paste it into the browser and perform an action on a website, then continue the flow in Postman.
The project manager, who initially created that tests, thought that Postman is for APIs only. 
But it´s for all kind HTTP requests, and this is basically what a browser is doing: Sending http requests, and displaying & rendering the returned HTML
With my previous web UI automation knowledge, I was able to bridge that gap and automate the whole flow in Postman, 
which enabled us to run the Postman tests via Continuous Integration.
Not the biggest progress in testing the API, but I learned a lot about Postman, and especially about Javascript.
Also, we could execute the tests fully automated and un-attended, without any manual interaction, and that was a great step forward.

Another example is my workflow in the first weeks for creating a test in Postman:
First I created only the request to create an item via the API, without any tests
I then added more requests to the workflow, for example to retrieve the newly created item from the API
I then added tests, for example to check if the requests return the correct http status code, if the created items are correct, and so on.
Next step was to parametrize the requests and the tests, 
for example the URL was unique per each client, so I introduced variables instead of hardcoding that values.
I left the difficult parts until the very end (for example how to iterate over a nested JSON Array with Javascript to check specific values within the JSON data)

To not bring something to perfection, but only to a good-enough-state, is an often used principle, 
and is applied in many engineering disciplines, and it also makes sense in software projects.

---

# Slide 16

**@chrissbaumann #EclipseCon**

### Notes
Another thing that can save you a lot of time, is to look out for patterns!

If you often have to do the same or similar tasks, 
it can make sense to setup a general structure or process, 
A kind of a blueprint that you can re-use

This can save you a lot of time.

---

# Slide 17

**@chrissbaumann #EclipseCon**

### Notes
The point is, you should not end up doing like the guy on the right.

During the course of the project, it turned out that we not only had to do performance testing in one sandbox environment, as it was initially announced.
But the luxembourgish regulator demanded, that the UAT environment of every client also needed to be performance tested and to be compliant with their performance requirements.
In our case, the UAT environments were a pre-production environment, which are linked to the client’s test environment, whereas the Sandbox environments only had a database with some fake test data.

By the way, let’s have a look at the requirements for that performance tests demanded by the regulator...

---

# Slide 18: Multiple merchants at the same time

Performance test requirements by the CSSF (Commission de Surveillance du Secteur Financier)
**@chrissbaumann #EclipseCon**

### Notes
Capability of the dedicated interface to support access by multiple merchants at the same time

This to ensure, that each merchant can only access the data of its own clients.
To me, this is more a functional than a performance requirement.

---

# Slide 19: Multiple merchants at the same time 
Extremely high numbers of requests

Performance test requirements by the CSSF (Commission de Surveillance du Secteur Financier)
**@chrissbaumann #EclipseCon**

### Notes
Capability of the dedicated interface to deal with extremely high numbers of requests

Ok, this makes sense for a performance test. But what is an “extremely high number”?
This was up for the clients to decide, and has lead us to some very interesting conversations, 
as some clients had really unrealistic ideas about what an “extremely high number of requests” is...

---

# Slide 20: Multiple merchants at the same time 
Extremely high numbers of requests 
Extremely high number of concurrent open sessions

Performance test requirements by the CSSF (Commission de Surveillance du Secteur Financier)
**@chrissbaumann #EclipseCon**

### Notes
Use of an extremely high number of concurrent open sessions (i.e. open at the same time)

This definitely makes no sense for an API, as there are no open session.
You send a request, you get a response, end of story.
But no sessions like in web applications for example.
Guess someone at the regulator simply copy pasted from some other template,
but as my colleagues could tell me from earlier experiences, 
arguing with the regulator about their requirements would have been totally pointless.

---

# Slide 21: Multiple merchants at the same time 
Extremely high numbers of requests 
Extremely high number of concurrent open sessions 
Requests for large volumes of data

Performance test requirements by the CSSF (Commission de Surveillance du Secteur Financier)
**@chrissbaumann #EclipseCon**

### Notes
Requests for large volumes of data

This one also makes sense… But what does “large” mean? 
The typical requests and responses for that API have a couple of kilobytes in size.
Initially we had a hard time to explain clients, that we don’t want to move Mega- or even Gigabytes of data, 
as that’s not a very realistic use case. But that was their idea of “large volumes of data”.

---

# Slide 22

**@chrissbaumann #EclipseCon**

### Notes
Back to me, trying to improve my process and toolset.

At first, we discussed the client’s needs for the performance tests in UAT with each client individually, 
leading to very different requirements for each client, especially concerning things like
“What is the duration of one performance test run?”
“How many parallel users should be used during a performance test run?”
“What is a large volume of data?”
“What’s an extremely high number of concurrent open sessions?”
And many many more…

Additionally, we didn’t use a proper performance test tool, but some command line tools, that simply executed the postman tests in parallel. 
Which was a nightmare to maintain, and also the reporting was pretty bad and required a lot of manual effort.
But initially, it was meant to be a one time thing, and thus ok.

It was -no surprise- not maintainable for more than 20 clients.
So I drafted performance tests for each of the criteria of the regulator in Jmeter and explained those in a document we handed out to the client.
A lot of values had been set by us, which avoided a lot of discussions with the clients.
Some values, like the number of parallel users per test, where based on the usage data of the client’s web banking, and those we asked the clients to provide us.

I then set up a little framework in the performance test tool JMeter, which I could easily re-use.
Values that changed per client could be adapted via a handful of config files with very little effort.

---

# Slide 23

**@chrissbaumann #EclipseCon**

### Notes
But be careful...

Getting things up and running and maintaining them can take a lot of time.

Don’t maintain a process or an automation solution just for the sake of maintaining something, 
but only do so, if you benefit from it.

The shown comic is about automating a repetitive task, with the intent to do a one time effort to automate that task and spend time in the long run.

But very often, the maintenance and further development of that automation, takes more time than it took to manually perform the initial task.

---

# Slide 24

**@chrissbaumann #EclipseCon**

### Notes
Another important thing to do is: Manage Expectations

What you should keep in mind, is that expectations are based on what has come before.
And because everybody has different experiences and thus different expectations, 
it’s important to make clear to stakeholders what to expect

Keep your stakeholders informed, because nobody likes surprises.
Talk to your stakeholders regularly and let them know what you achieved and what you’ll achieve next, 
Try to give them a timeline. Yes, estimates are difficult. 
But I’m not talking about absolute figures and promises here, but about when you think you can achieve what.
Make clear that you’re giving estimates, not promises.

Involving people earlier versus surprising them, is very effective over time, 
for both, building trust and for managing expectations more effectively.

Also, you need to clearly articulate the risks you see.
You should report obstacles, and especially if you think, something is not feasible, 
that you for example cannot reach a deadline,
or might not be able to acquire the necessary knowledge in the given time

Finally: Have a Backup plan.
This helps to set the frame that things can go wrong, and if they do, nobody is surprised.
And if things goes wrong, you are prepared.
It also shows you’ve thought through the problem. 

---

# Slide 25

**@chrissbaumann #EclipseCon**

### Notes
Besides all the advices and hints how to work on such a project, it’s also very important that you stay healthy

For that, you should try to not get overwhelmed by your work!

Leave work at work, and don’t take it home
Let me share a story from a project where I was not able to do so:
I was a test project lead for the very first time in my career and the project was doomed from the very first day, but me as a newby was not able to see that back then.
It was a project in waterfall mode, and there was an intensive two weeks testing phased scheduled, which meant subject matter experts and testers were locked into a room, to “test quality” in.
This project was so very much eating me up, I had a notepad and pen on my nightstand, because I woke up in the middle of the night, thinking about stuff I didn’t want to forget, so I could write that down.
It was a very stressful time and not healthy at all and over time I learned to leave work at work.

In general: Don’t get into the hamster wheel (Alex Schladebeck and Huib Schoots gave an impressive keynote about that at Agile Testing Days 2018, you can find a recording of it on Youtube)

So much for my experiences, how I handled the challenges and what else can work in such a situation,

Let’s talk about some more general “How to” questions

---

# Slide 26

**@chrissbaumann #EclipseCon**

### Notes
How do you avoid such situations?

Are there other people that can help out, that can join or support the project?
- Can you find them Inside your own organization? In your team? In different teams or departments?
- Or maybe you need to look outside of your organization: Should someone be hired? Can part of the work be outsourced or does it make sense to bring consultants on board?

If you believe, that you’re in such a project: Make it clear right from the beginning, that it is impossible to succeed, but give detailed reasons for why this is the case.

---

# Slide 27

**@chrissbaumann #EclipseCon**

### Notes
How do you recognise and talk about such projects?

Ask questions
Like
Do we have the right people & skills?
Whom do we have to get onboard?
How much do we have to learn?
What are the deadlines to provide results?
Is that feasible?

If you’re already “caught” in such project, try to step back, get out of the hamster wheel and make yourself aware that you ARE in such a project.

Talking about such projects in your organisation can be difficult, depending on the company culture,
but you have to raise it anyhow, because "If you don't speak up, there's a 100% chance of nothing to be changed"

---

# Slide 28

**@chrissbaumann #EclipseCon**

### Notes
Finally: How to prevent such projects?

The mandatory precondition for prevention is, that you need to have recognised that such a project is gonna happen.
And! you need to talk about it.

What I said about expectation management earlier is key.
Manage expectations and take actions to execute the project better

---

# Slide 29

Thank you! Questions?
**@chrissbaumann #EclipseCon**

### Notes
That was my talk, many thanks for your attention.

I hope you found some useful bits for your work.

I’m happy to answer any questions you might have.

---

# Slide 30: Ressources

https://cirkus.com/blog/multitasking-skills/
https://fairygodboss.com/articles/multitasking-at-work
https://sourcesofinsight.com/expectation-management/
https://www.goodreads.com/book/show/7117789-pomodoro-technique-illustrated
https://www.wikihow.com/Multitask
https://yaro.blog/8750/expectation-management/  https://www.youtube.com/watch?v=EElajYi6mtU
**@chrissbaumann #EclipseCon**

---

# Slide 31: Images

commons.wikimedia.org/wiki/File:Too_Busy_To_Improve\_-\_Performance_Management\_-\_Square_Wheels.png
de.wikipedia.org/wiki/Laufrad\_(Kleintier)#/media/Datei:Phodopus_sungorus\_-\_Hamsterkraftwerk.jpg
pexels.com/de-de/foto/altes-buch-antik-antiquitat-ausstellungsstuck-1172018/
pexels.com/de-de/foto/ausbildung-brettspiel-challenge-damebrett-260024/
pexels.com/de-de/foto/ausrustung-begrifflich-berg-draussen-2853432/
pexels.com/de-de/foto/bank-stadt-fashion-mann-3867509/
pexels.com/de-de/foto/brett-bullauge-center-darts-226579/
pexels.com/de-de/foto/kunst-kreativ-strasse-graffiti-4552137/
pxfuel.com/en/free-photo-eibzf
pxfuel.com/en/free-photo-embkb
pxfuel.com/en/free-photo-eofzx
pxfuel.com/en/free-photo-qecwy
pxfuel.com/en/free-photo-xptq
pxhere.com/en/photo/1099398
pxhere.com/en/photo/1255571
pxhere.com/en/photo/759410
pxhere.com/en/photo/962909
xkcd.com/1319/
**@chrissbaumann #EclipseCon**
