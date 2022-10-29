## Structure

I just have a bunch of functions in `test.py` that always save their result in a file, so I can skip computing-expensive steps later.

## References

*Maybe* put the links in here next time, asshole. Using the one I am finding now:

* [Recommendation System Using Matrix Factorization](https://www.aurigait.com/blog/recommendation-system-using-matrix-factorization/) seems like a good intro & tutorial. Ok, maybe not tutorial. He does wild shit.
* [This one](https://towardsdatascience.com/recommendation-system-matrix-factorization-d61978660b4b) moves fairly slowly but does pure math. *Probably* would be wise, to, you know, just understanding this. "Just". Oh, and he does have a practical Python code. Let's try.

## Problems

### The matching id and titles story ark

Right now I am getting book IDs out (as a recommendation for a hard coded book), and rather silliely, failing to match them back to book titles.
The ids are also kind of sus, are they counts or something?

I do have a sanity check for this. Cool. Vaguely seems to check out.

Next question: Why the fuck *can* this even possibly happen? How is this not the same data?

Ok. Now very sure. The title finder for a random id works. The problem is that what comes back from the recommendation algo are in fact not ids but probably...indices!

I think *a* problem is that I have no idea what the recommendation getter actually does. So here is the semi-stolen, semi copilotted old line:

 `distances, suggestions = model.kneighbors(book_pivot.iloc[book_idx, :].values.reshape(1, -1))`

 Ok. Now I am pretty sure I am getting user ids. lol. Here is the code I am using:

```
# use kneighbors to get the ids of the 10 closest matches to the book
distances, indices = model.kneighbors(book_pivot.iloc[book_idx, :].values.reshape(1, -1), n_neighbors=n_recommendations+1)
# get the book ids of the 10 closest matches
book_ids = book_pivot.index[indices.flatten()]
# make a normal list
book_ids = book_ids.tolist()
```

Ok. `stealing/denise2.py` now has a working matrix factorization going on. Next I need to think about how to get this into a working/useful 'recommend me books thing'. Need a break.