/*jshint esversion: 8 */
/*jshint node: true */

const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

const dealerships_file = fs.existsSync(__dirname + "/dealerships.json") ?
  __dirname + "/dealerships.json" : __dirname + "/data/dealerships.json";

const reviews_file = fs.existsSync(__dirname + "/reviews.json") ?
  __dirname + "/reviews.json" : __dirname + "/data/reviews.json";

const reviews_data = JSON.parse(fs.readFileSync(reviews_file, 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync(dealerships_file, 'utf8'));

let localReviews = [...reviews_data.reviews];
let localDealerships = [...dealerships_data.dealerships];

let mongoConnected = false;
mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB', serverSelectionTimeoutMS: 2000 })
  .then(() => {
    mongoConnected = true;
    console.log("Connected to MongoDB");
    Reviews.deleteMany({}).then(() => {
      Reviews.insertMany(reviews_data.reviews);
    });
    Dealerships.deleteMany({}).then(() => {
      Dealerships.insertMany(dealerships_data.dealerships);
    });
  })
  .catch((err) => {
    console.log("MongoDB connection unavailable; using local JSON data store.");
  });

const Reviews = require('./review');
const Dealerships = require('./dealership');

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    if (mongoConnected) {
      const documents = await Reviews.find();
      return res.json(documents);
    }
  } catch (error) {}
  res.json(localReviews);
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    if (mongoConnected) {
      const documents = await Reviews.find({ dealership: req.params.id });
      return res.json(documents);
    }
  } catch (error) {}
  const filtered = localReviews.filter(r => String(r.dealership) === String(req.params.id));
  res.json(filtered);
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    if (mongoConnected) {
      const documents = await Dealerships.find();
      return res.json(documents);
    }
  } catch (error) {}
  res.json(localDealerships);
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    if (mongoConnected) {
      const documents = await Dealerships.find({ state: req.params.state });
      return res.json(documents);
    }
  } catch (error) {}
  const filtered = localDealerships.filter(d => d.state && d.state.toLowerCase() === req.params.state.toLowerCase());
  res.json(filtered);
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    if (mongoConnected) {
      const documents = await Dealerships.find({ id: req.params.id });
      return res.json(documents);
    }
  } catch (error) {}
  const filtered = localDealerships.filter(d => String(d.id) === String(req.params.id));
  res.json(filtered);
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    let data;
    if (typeof req.body === 'string') {
      data = JSON.parse(req.body);
    } else if (Buffer.isBuffer(req.body)) {
      data = JSON.parse(req.body.toString('utf8'));
    } else {
      data = req.body;
    }

    let new_id = localReviews.length > 0 ? Math.max(...localReviews.map(r => r.id || 0)) + 1 : 1;

    const reviewObj = {
      id: new_id,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    };

    localReviews.push(reviewObj);

    if (mongoConnected) {
      const review = new Reviews(reviewObj);
      const savedReview = await review.save();
      return res.json(savedReview);
    }
    res.json(reviewObj);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
