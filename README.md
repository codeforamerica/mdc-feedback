# mdc-feedback
[MDC Fellowship 2015] Feedback Engine. Details TBA

## Wireframes

![feedback_flow_v1-1](https://cloud.githubusercontent.com/assets/33945/8314560/11a67eca-199f-11e5-8625-38d84fb028f4.png)
![feedback_flow_module_v1-1](https://cloud.githubusercontent.com/assets/33945/8314562/1552bd5e-199f-11e5-81d8-9fe0d34ea8c6.png)
![feedback_flow_v1-2](https://cloud.githubusercontent.com/assets/33945/8314566/1b1f0d46-199f-11e5-86bc-4859df9ed84c.png)

![feedback_backend](https://cloud.githubusercontent.com/assets/33945/8315038/7e7d3964-19a2-11e5-9e70-ebf7afb7a7b0.png)
![feedback_backend_3](https://cloud.githubusercontent.com/assets/33945/8315040/7e82d702-19a2-11e5-9d11-08d7eb77fa51.png)
![feedback_backend_4](https://cloud.githubusercontent.com/assets/33945/8315039/7e7df9ee-19a2-11e5-8208-6671a3c8da96.png)

## Screenshots

![First prototype screenshot](https://www.evernote.com/shard/s29/sh/69bd40c1-b1fd-4d8a-97c0-09876ce3b50e/e09856405ea1a320/res/14a07f0c-e1d7-47f7-9830-a1760bcbcb0e/skitch.png?resizeSmall&width=832)

To run on localhost (for your own sanity):
`python manage.py runserver`

`mkvirtualenv mdc-feedback`
`workon mdc-feedback`

`git push heroku master`

https://realpython.com/blog/python/flask-by-example-part-1-project-setup/

`python manage.py db migrate -m "Initial migration"`

https://cfa.typeform.com/to/UYZYtI
API key: 433dcf9fb24804b47666bf62f83d25dbef2f629d
https://api.typeform.com/v0/form/UYZYtI?key=433dcf9fb24804b47666bf62f83d25dbef2f629d&completed=true

```
Is the database empty?
If so, import everything into the db table
else
  see the last entry in the database
```
