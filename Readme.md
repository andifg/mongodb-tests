# Mongodb Schema tests

This repo is a test repo to try out different schema options as well as 
different query possibilities for mongodb

# Start Mongodb database

```bash
docker-compose up
```

# Normalized Schema Performance 

## aggregate_normalized_ratings_and_coffees

### Limit 10, 3000 coffees, 444612 ratings

Without index -> 3 seconds

With index on coffee-id in the rating schema -> 40ms

### Limit 50, 3000 coffees, 444612 ratings

Without index -> 13 seconds

With index on coffee-id in the rating schema -> 50ms

### Limit 50, 3000 coffees, 599504 ratings

Without index -> 13 seconds

With index -> 35ms
With index -> 40ms