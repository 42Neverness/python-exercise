import nltk
from nltk.corpus import gutenberg
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
from textblob import TextBlob

# Download necessary NLTK data
nltk.download('gutenberg')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Step 1: Read Moby Dick file from the Gutenberg dataset
moby_dick_tokens = gutenberg.words('melville-moby_dick.txt')

# Step 2: Tokenization
tokens = word_tokenize(' '.join(moby_dick_tokens))

# Step 3: Stopwords Filtering
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

# Step 4: Parts-of-Speech (POS) Tagging
pos_tags = nltk.pos_tag(filtered_tokens)

# Step 5: POS Frequency
pos_counts = FreqDist(tag for word, tag in pos_tags)
top_pos = pos_counts.most_common(5)
print("Top 5 Parts of Speech and their counts:")
for pos, count in top_pos:
    print(f"{pos}: {count}")

# Step 6: Lemmatization
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'  # Adjective
    elif treebank_tag.startswith('V'):
        return 'v'  # Verb
    elif treebank_tag.startswith('N'):
        return 'n'  # Noun
    elif treebank_tag.startswith('R'):
        return 'r'  # Adverb
    else:
        return 'n'  # Default to noun

lemmatized_tokens = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in pos_tags[:20]]

# Step 7: Plotting Frequency Distribution
pos_counts.plot(20, title='POS Frequency Distribution')
plt.show()

# Step 8: Sentiment Analysis (Optional)
def calculate_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

average_sentiment = calculate_sentiment(' '.join(filtered_tokens))
overall_sentiment = "positive" if average_sentiment > 0.05 else "negative"
print(f"\nAverage Sentiment Score: {average_sentiment}")
print(f"Overall Text Sentiment: {overall_sentiment}")
