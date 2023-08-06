# `namedtuple` Maker

![GitHub Actions Status](https://img.shields.io/github/workflow/status/wwt/devasc-data-formats/Markdown%20Linting?logo=github "GitHub Actions Status")

## Easily Convert Python iterable objects into `namedtuple` objects

### Contents

- [Capabilities](#capabilities "Capabilities")
- [Requirements](#requirements "Requirements")
- [Installation](#installation "Installation")
- [Usage](#usage "Usage")
- [Background](#background "Background")
- [`namedtuple` objects and The Zen of Python](#namedtuple-objects-and-the-zen-of-python "The Zen of Python")

---

### Capabilities

- Converts Python iterable objects (`list`, `tuple`, `set`, etc.) into a `namedtuple` objects using a decorator function, **so you don't have to rewrite code that already returns iterable objects**.

- Gathers `namedtuple` attribute names via either a `kwarg` in a decorated function or using prompts to collect attribute names.

- Automatically corrects attribute name entries that would be invalid.

---

### Requirements

- Python 3.9+

---

### Installation

Install via Python pip:

```bash
pip install namedtuple-maker
```

---

### Usage

#### Usage as a Decorator

<details><summary><b>Click to expand and view a decorator example</b></summary>

1. Create an iterable object:

    ```python
    my_favorites = (
        'pizza',
        'summer',
        'too personal'
    )
    ```

2. Import the `convert_to_namedtuple` decorator function:

    ```python
    from namedtuple_maker.namedtuple_maker import named_tuple_converter
    ```

3. Create a function that returns an iterable object, and decorate that function with the `convert_to_namedtuple` decorator function:

    ```python
    @named_tuple_converter
    def tuple_to_namedtuple(
        iterable_input=my_favorites,
        attribute_names=None
    ):

        return iterable_input
    ```

4. Call the `tuple_to_namedtuple` function:
    - Pass an iterable object (the default `my_favorites` object, in this example) to the `iterable_input` parameter.
    - By default, you will receive a prompt to provide an attribute name for each iterable input value.
    - You may instead pass a separate iterable object of attribute names to the `attribute_names` parameter.

    <details><summary>Option #1 - Enter attribute names using prompts:</summary>

    ```python
    # Call the tuple_to_namedtuple function and fill the attribute name prompts
    my_named_favorites = tuple_to_namedtuple()
    ```

    ```text
    Enter an attribute name for the value "pizza": food
    Enter an attribute name for the value "summer": season
    Enter an attribute name for the value "too personal": sports team
    ```

    </details>

    <details><summary>Option #2 - Pass an iterable object of attribute names to the `attribute_names` parameter:</summary>

    ```python
    # Create an iterable object with attribute names
    my_attributes = (
        'food',
        'season',
        'sports team'
    )

    # Call the make_named_tuple function and pass in the attribute names
    my_named_favorites = tuple_to_namedtuple(
        attribute_names=my_attributes
    )
    ```

    </details>

5. Display the resulting `namedtuple` object:

    ```python
    print(my_named_favorites)
    ```

6. Observe the `print` function output:

    ```text
    NamedTuple(food='pizza', season='summer', sports_team='too personal')
    ```

</details>

---

#### Usage as a Function

<details><summary><b>Click to expand and view a function usage example</b></summary>

1. Create an iterable object:

    ```python
    my_favorites = (
        'pizza',
        'summer',
        'too personal'
    )
    ```

2. Import the `make_named_tuple` function:

    ```python
    from namedtuple_maker.namedtuple_maker import make_named_tuple
    ```

3. Call the `make_named_tuple` function:
    - Pass an iterable object (the default `my_favorites` object, in this example) to the `iterable_input` parameter.
    - By default, you will receive a prompt to provide an attribute name for each iterable input value.
    - You may instead pass a separate iterable object of attribute names to the `attribute_names` parameter.

    <details><summary>Option #1 - Enter attribute names using prompts:</summary>

    ```python
    # Call the make_named_tuple function and fill the attribute name prompts
    my_named_favorites = make_named_tuple(
        iterable_input=my_favorites
    )
    ```

    ```text
    Enter an attribute name for the value "pizza": food
    Enter an attribute name for the value "summer": season
    Enter an attribute name for the value "too personal": sports team
    ```

    </details>

    <details><summary>Option #2 - Pass an iterable object of attribute names to the `attribute_names` parameter:</summary>

    ```python
    # Create an iterable object with attribute names
    my_attributes = (
        'food',
        'season',
        'sports team'
    )

    # Call the make_named_tuple function and pass in the attribute names
    my_named_favorites = make_named_tuple(
        iterable_input=my_favorites,
        attribute_names=my_attributes
    )
    ```

    </details>

4. Display the resulting `namedtuple` object:

    ```python
    print(my_named_favorites)
    ```

5. Observe the `print` function output:

    ```text
    NamedTuple(food='pizza', season='summer', sports_team='too personal')
    ```

</details>

---

### Background

Python `tuple` objects are great, right?  So are `list`, `set`, and many other iterable Python objects. However, accessing the values of an iterable object using arbitrary index numbers can make code difficult to read.  For example, the following `list` object stores data about the foods I might eat in a given day:

```python
my_meals = [
    'pizza',
    'blueberry pancakes',
    'granola',
    'fruit smoothie',
    'rice and beans'
]
```

Let's say that I want to access values in the `list` object named `my_food`. I can do that by referencing one or more numeric **list indices** like this:

```python
print('My Meals')
print('--------')
print(f'Breakfast: {my_meals[1]}\n'
      f'Snack: {my_meals[3]}\n'
      f'Lunch: {my_meals[4]}')
```

The resulting output from this code is:

```text
My Meals
--------
Breakfast: blueberry pancakes
Snack: fruit smoothie
Lunch: rice and beans
```

That works just fine, although it's not terribly intuitive to associate a `list` (or `tuple`) **index number** with a certain meal of the day, since this `list` doesn't have meals in any particular order. The list index assigned to each meal is _arbitrary_.

---

### The Python `namedtuple` Function

The `collections` module in the Python Standard Library includes the [`namedtuple` function](https://docs.python.org/3/library/collections.html#collections.namedtuple), which allows you to, as the name implies, create tuple-like objects with values that you can reference by name.  What does that mean, practically? Well, it means you can access the values in an iterable object by an _explicit_ **attribute name** that is much more meaningful than an _arbitrary_ **index number**.

For example, I'll recreate the `my_meals` data using a `namedtuple` object:

1. First, import the `namedtuple` function from the `collections` module:

    ```python
    from collections import namedtuple
    ```

2. Next, create a new object type using the `namedtuple` function.
    - Think of a `namedtuple` object like a `class` object with named attributes, but no methods.
    - The `typename` parameter is an arbitrary name for the object class.
    - The `field_names` parameter defines the attribute names for the new object.

    ```python
    Meals = namedtuple(
        typename='Meals',
        field_names=[
            'breakfast',
            'snack',
            'lunch',
            'dinner',
            'dessert'
        ]
    )
    ```

3. Now, create an instance of the `Meals` object, and assign the individual foods to each of the named attributes (specified by the `field_names` parameter):

    ```python
    my_meals = Meals(
        breakfast='blueberry pancakes',
        snack='fruit smoothie',
        lunch='rice and beans',
        dinner='pizza',
        dessert='granola'
    )
    ```

When I want to access or display data from the `namedtuple` object named `my_meals`, my code will look something like this:

```python
print('My Meals')
print('--------')
print(f'Breakfast: {my_meals.breakfast}\n'
      f'Snack: {my_meals.snack}\n'
      f'Lunch: {my_meals.lunch}')
```

The result from this code looks exactly like it did in the first example:

```text
My Meals
--------
Breakfast: blueberry pancakes
Snack: fruit smoothie
Lunch: rice and beans
```

The key difference between the `list` example and the `namedtuple` example is, accessing the values in the `namedtuple` object uses _explicit_ **named attributes** (`my_meals.lunch`), rather than _arbitrary_ **index numbers** (`my_meals[4]`).

For me, it's much easier to remember that the food I ate for breakfast is accessible as `my_foods.breakfast` within a `namedtuple` object, than it is to remember an arbitrary `list` index value like `my_foods[3]`.

---

### `namedtuple` objects and The Zen of Python

The [Zen of Python](https://www.python.org/dev/peps/pep-0020/ "Zen of Python") is a great guide for how to write clean and effective Python code. Below is an extract of some of the lines in the output of an `import this` command.

The intent of the `named-tuplemaker` package is to help Python developers write code that improves compliance with The Zen of Python by making it simple and easy to access iterable object values by _explicit_ **attribute names**, rather than _arbitrary_ **index numbers**.

```text
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
...
Readability counts.
...
```
