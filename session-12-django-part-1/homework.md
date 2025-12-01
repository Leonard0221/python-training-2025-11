# Python Interview Questions & Coding Challenges - Session 12

## Concept Questions

- What is Django's MTV pattern? 
  - Django uses the Model-Template-View (MTV) pattern, which is Django's take on the classic MVC (Model-View-Controller) architecture.
    - Model: This is the data access layer. It defines the structure of your data (fields and relationships) and handles all database interactions.
    - Template: This is the presentation layer. It dictates how the data is rendered to the user, typically as an HTML file with Django Template Language (DTL) logic.
    - View: This is the business logic layer. It acts as the "controller" by receiving the request, interacting with the Model to process data, and then selecting and rendering a Template for the final response.

- What's the difference between blank=True and null=True?
  - null=True: relates to the database. It allows the field's column in the database schema to store a NULL value, which is appropriate for non-string fields like IntegerField or DateTimeField.
  - blank=True relates to validation. It permits an empty value (an empty string or no selection) to be accepted when a form or the Django Admin validates the data. For string-based fields, it’s best practice to use blank=True and set a default of '' rather than using null=True.

- What's the difference between auto_now and auto_now_add?
  - auto_now = True: This field is updated every time the model object is saved. It's used for tracking the last time an object was modified (e.g., a modified_at field).
  - auto_now_add=True: This field is set only when the object is first created and cannot be manually modified thereafter. It's used for recording the creation timestamp of an object (e.g., a created_at field).

- What are Django migrations and why are they important?
  - Django Migrations are Django's system for propagating changes made to your Models (your data structure) into your database schema.
  - They are essential because they:
    - Version Control the Database: They provide a history of schema changes, allowing you to reliably move your database structure forward and backward.
    - Ensure Consistency: They ensure that all developer and production environments use the exact same schema defined by your models.
    - Allow Evolution: They let you safely modify the database structure over time without losing existing data.

- What is the N+1 query problem? How to avoid it in Django
  - The N+1 query problem is a performance issue where fetching related objects leads to one initial query to retrieve N parent objects, followed by N separate queries to fetch the related data for each parent object, resulting in N+1 total database hits.
  - To avoid this in Django, we use QuerySet optimization methods to fetch all necessary related data in a single, efficient operation:
    - select_related(): Used for ForeignKey and OneToOne relationships (one-to-many/one-to-one). It performs a single JOIN operation at the database level.
    - prefetch_related(): Used for ManyToManyField and reverse ForeignKey relationships (many-to-many/many-to-one). It performs a separate lookup query for each relationship and joins the results in Python memory.

- What is the Meta class in Django models?
  - The Meta class is an inner class defined within a Django model that is used to provide metadata about the model that is not field-specific.
  - Common uses include:
    - ordering: Defining the default order of objects when querying the model.
    - verbose_name / verbose_name_plural: Providing human-readable names for the model.
    - unique_together: Enforcing uniqueness across a specific combination of fields.

- What's the purpose of __str__() method in models?
  - The __str__() method returns the official string representation of a model object. Its primary purpose in Django is to provide a meaningful, human-readable name for an object instance.
  - It is crucial for:
    - Django Admin: The Admin interface uses this method to display related objects in dropdown menus and object listings.
    - Debugging and Logging: It makes model instances easy to identify when printed or logged, for example, showing a post's title instead of a generic object reference like <Post object (id=1)>.


## Coding Challenge:

### 1. Implement the Blog app on your own
Follow the quick reference guide to create the blog app on your local step by step

### 2. Django ORM practice
```
# Write these queries in shell and save the output:

# 1. Get all published posts
# 2. Get all posts by user 'john'
# 3. Get all posts in "Technology" category
# 4. Count total posts
# 5. Count total comments
# 6. Get posts with no categories
# 7. Get the 3 newest posts
# 8. Get all categories sorted alphabetically
```

### 3. Add a View Counter
- Step 1: Update Model to add a views integer field
- Step 2: Create & Run Migration
- Step 3: Increase the post views when the post_detail view is processed
- Step 4: Update Admin to show post views
- Step 5: Show in Template
```html
<!-- In post_detail.html, add: -->
<div class="meta">
    {{ post.views }} views
</div>
```


### 4. Add Custom Model Methods
- Add These Methods to Post Model
``` python
def get_excerpt(self):
    """Return first 100 characters of content"""

def published_recently(self):
    """Check if published in last 7 days"""

def has_multiple_categories(self):
    """Check if post has more than one category"""
```

- Use in Templates:
```html
<!-- In index.html: -->
<p>{{ post.get_excerpt }}</p>

{% if post.published_recently %}
    <span class="badge">🆕 New!</span>
{% endif %}
```

- use in Admin:
``` python
# Add to PostAdmin list_display:
def is_new(self, obj):
    return obj.published_recently()
is_new.boolean = True
is_new.short_description = 'Recent?'
```



