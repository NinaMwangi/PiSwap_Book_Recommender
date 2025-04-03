# Pi Swap

Pi Swap is an app that uses ML recommender systems to give users recommendations based on their ratings and interactions with books. The model aims to alleviate the cost of education, promote environmental sustainability, and promote the idea of cyclical economies by reducing over-consumerism and encouraging reusing. The methodology used in this model is the use of recommender systems. This model as a proposed solution can in the future be incorporated into a web application and a mobile application to create a platform that serves as an online marketplace where parents and students can buy and sell second-hand books.

The Dataset

## Content

The dataset comprises 3 files.

**Users**: Contains the users. Note that user IDs (User-ID) have been anonymized and map to integers. Demographic data is provided (Location, Age) if available. Otherwise, these fields contain NULL-values.
**Books**: Books are identified by their respective ISBN. Invalid ISBNs have already been removed from the dataset. Moreover, some content-based information is given (Book-Title, Book-Author, Year-Of-Publication, Publisher), obtained from Amazon Web Services. Note that in cases of several authors, only the first is provided. URLs linking to cover images are also given, appearing in three different flavours (Image-URL-S, Image-URL-M, Image-URL-L), i.e., small, medium, and large. These URLs point to the Amazon website.
**Ratings**: Contains the book rating information. Ratings (Book-Rating) are either explicit, expressed on a scale from 1-10 (higher values denoting higher appreciation), or implicit, expressed by 0.
The dataset is from Kaggle. https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset

## Demo Link

## How to set up the Application
1. Access the docker-compose.yaml file
2. Run `docker compose up --build docker-compose.yaml`
3. Go to the browser and run http://localhost
4. Once on the web app you will have two sections.
5. The first button is for uploading data that triggers retraining.
6. The second button is the recommend button where you input a book name and it recommends similar books.
