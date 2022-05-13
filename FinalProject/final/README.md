# CS Skill Tracker

### Intro
#### *CS stands for Computer Science*
This app is created as a small scale blog where I journal my learning and run-ins while learning new technologies. The intent is to keep  myself accountable for learning something new regarding computer science at least once a day. Afterwards, it will be visualized in different ways such as EXP progress bars. 

---

### Inspiration
I personally went through many gamified apps that focused on habit and routine building.  The novelty wore off for me very quickly as well as it was difficult to have friends be on the same app. Because it "another app to install sitting somewhere". 

---

### Objective: Gamified UI/UX Design 
The main focus is to have this mobile-friendly as much as possible especially as visually-rich as intended. Visualizing user inputted data will give the user a sense of accomplishment - At least I think so. Most of the novelty wears off with apps that can do the same thing. The objective is to make sure it is seamless and effort can be immediately rewarded.

---

### Architecture
#### Organization
``Forms`` are in its py file as well as ``Models`` are in its own py file. Things like this made organization easier overall. Before that, I did not know it was a thing to do.

#### More ManytoManyRelationships
Unlike the Network project, using a ForeignKey was the fastest implementation for a like button and following/followers. ManytoManyRelationships are heavily emphasized here for tags and likes. Tags could have been as simple as selecting from a list but that will not scale well. Also, less processing time with fewer tables in the databases would be the most efficient. 

#### ``forms.Forms`` vs ``forms.ModelForm``
I have changed the way the code is organized for my for forms because ModelForm will at least make a form based based on the scehema of the database. More preferred having a manually made form that does not interact with the database. The database is most certainly  needed for a blog-like app.

#### Bootstrap with SASS/SCSS
I am definitely no UI/UX designer. Good thing Bootstrap has taken care of this. I also wanted more customization by implementing SASS as well. This involves installing a dependency that allows it compress  and  talks to Bootstrap's SASS. 

*Resources:*

- [Sass Bootstrap v5.0](https://getbootstrap.com/docs/5.0/customize/sass/)
- Free themes for Bootstrap: [Bootswatch] (https://bootswatch.com/)
- [Sass Basics](https://sass-lang.com/guide)


#### Python vs JavaScript: Who Handles The  Logic?
I wanted JavaScript to only handle what is seen from the client-side and the logic handling is in the back-end (Python). This was done via serializing/de-serializing JSON back and forth. For example, for the like button, the logic will take data from Django's template tag (an ID) and have it check for True or False. Afterwards, Javascript will manipulate the DOM to show the correct status and icon. 

---

### Features
- Like
- Comment
- Blog
- Tagged Posts

---

### Implementations That Did Not Make it
- HTML Calendar
  - Linking a post to a day to see from a visual perspective
  - Reminders to post once a day as a modal/pop-up or email
- Progress Bars
  - Where the number of posts determines how much of the bar is filled. The completion of the bar is arbitrary and up to the user. It is best used if it is a montly goal of 30 days of knowledge gaining
  - Afterwards, the user can use it as a milestone and write down concepts in a summarized tagged post cloud
- Animations (with Javascript)
  - This was a nice-to-have
  - I have came to the conclusion would probably take me at least month to understand and use ``anime.js`` - the JavaScript animation engine

---

### Future Implementation
- All of the above!
- Better understanding of software architecture beyond refactoring code
- Better UI/UX

---