# Week 4 Notes

I must say, dbt is pretty cool.  The jinja, the sql, how modular dbt is and the documentation rendering is really something.  I'm really interested in leaning into dbt in the future and definately want to practice with the core version.  

Having said that I found that Victoria really hits the ground running and I would recommend going to dbt and signing up for their [course account](https://courses.getdbt.com/collections) and running through the fundamentals course and the jinja, macros, packages course.  It's really well done, makes it really easy to understand dbt and in the end you get a badge for your linkedin.

This week wasn't particularly difficult but it was a load of fun.  For anyone following along this repo will know I had to go back and fix my week 2 and 3 airflow but once I got the data straigh this week was good.

One cautionary note is how you impelement week 4 into your github repo.  I kinda messed this up because I wanted the dbt files in a folder named week_4 on master.  So I moved all the dbt file into a folder named week_4 but then my production environment couldn't find the files.  To solve this I kept the week_4 on master just to make the repo look whole but I created a week_4_dbt branch to run the production environment.  

If you are interested in this method there are a couple things:

- The production branch needs a different name or dbt will get confused, hence week_4_dbt.
- When setting up the production environment you can select custom branch and then put `week_4_dbt` in there.

I didn't do any of the data studio stuff.  I did a bunch of data studio stuff in the past so I kinda skipped out on the charts.
