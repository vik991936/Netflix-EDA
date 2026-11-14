

# 📊 Netflix Exploratory Data Analysis (EDA) – Key Insight

## 1. Content Composition (Movies vs. TV Shows)

Movie Dominance: Movies make up the majority of Netflix’s catalog at 70.4%, while TV Shows account for 29.6%.
Portfolio Takeaway: While Netflix started heavily focused on films, TV shows have become a crucial strategic driver for user retention, despite lower raw counts.

## 2. Content Release & Platform Growth Trends
   
Explosive Growth Era (2015–2019): Content production and platform additions scaled exponentially starting around 2015, peaking sharply around 2018–2019 before experiencing a slight downward adjustment in later years.

Recent vs. Classic Content Gap: The vast majority of content are added to Netflix within 0 to 3 years of their original release year. However, a long-tail distribution shows that older classic catalog content is also regularly acquired.

Monthly Additions Seasonality: Content additions are distributed fairly evenly throughout the year, with slight bumps during mid-year (July) and year-end (December).

## 3. Geographic Distribution & Demographics

Top Producing Countries: The United States leads content production by a massive margin, followed by India and the United Kingdom. Other major contributors include Canada, France, Japan, and South Korea, highlighting a strong global footprint.

Audience Ratings: The platform leans heavily toward mature audiences, with TV-MA and TV-14 being the most frequent rating categories by a wide margin. This indicates that Netflix's primary target audience consists of teens and adults.

## 4. Genres, Directors, and Cast

Top Genres: International Movies, Dramas, and Comedies are the most prominent genres on the platform, reinforcing Netflix’s globalized content strategy.

Key Contributors: Directors like Rajiv Chilaka and Jan Suter, and actors like Anupam Kher and Shah Rukh Khan, feature heavily in the upper ranks of appearances, reflecting high volumes of regional and animation output.

## 5. Content Freshness Strategy (Content Age)

Focus on New Releases: Over 4,700 titles (more than half of the analyzed library) are added to Netflix within 0–1 year of their original release, classified as "New" content.

The "Classic" Bump: Interestingly, Catalogue content (10+ years old) outnumbers Older content (6–10 years old) (~1,200 vs. ~900 titles).

Portfolio Takeaway: Netflix follows a "barbell" acquisition strategy—investing heavily in brand-new releases/originals to attract subscribers while licensing proven, older classics (10+ years) rather than mid-tier aging content.

## 6. The Shifting Mix: Movies vs. TV Shows Over Time

TV Shows Gaining Ground: While Movies have always led in raw volume, the normalized percentage share chart shows that TV Shows steadily grew from ~24% of annual additions in 2018 to nearly 34% by 2021.

Portfolio Takeaway: Using percentage share instead of raw counts reveals a clear strategic pivot toward serialized TV content to boost long-term subscriber retention.

## 7. Regional Content Localization (US vs. India & Global Mix)

(a). Distinct Regional Strategies: Comparing the top two producing nations reveals opposite catalog priorities:

United States: Heavily weighted toward Dramas, Comedies, Documentaries, and Children & Family Movies.
India: Dominated overwhelmingly by International Movies and Dramas, with minimal presence in documentaries or kids' content.

(b). Country-Specific Niches (Heatmap): Normalizing genre share by country highlights regional specializations:

South Korea (53%) and Japan (42%) focus heavily on International TV Shows (driven by K-Dramas and Anime).
India (35%) and Spain (33%) index highest in International Movies.

## 8. Audience Targeting by Content Type
    
Adults & Teens First: Grouping individual ratings into broader audience tiers shows that Adults and Teens account for over 70% of both Movies and TV Shows.

Higher Kids Share in TV: TV Shows have a noticeably larger proportion of Kids content (~17%) compared to Movies (~7%), whereas Movies carry a larger share of Family content.

## 9. Movie Duration Trends & Genre Outliers

Movies Are Getting Shorter: From 1980 to 2020, the average movie runtime on Netflix steadily declined from roughly 120–125 minutes down to ~92–96 minutes.

Genre Runtime Patterns (Boxplots):

Shortest Formats: Generic Movies (~45 mins) and Stand-up Comedy (~67 mins) are significantly shorter than traditional feature films.

Longest Formats: Classic Movies, Action & Adventure, and Dramas average around 113–118 minutes.

High Variance & Outliers: Genres like Dramas, International Movies, and Sci-Fi & Fantasy contain extreme long-runtime outliers exceeding 250–300 minutes (likely multi-part theatrical releases or extended editions).

## 10. TV Show Duration & Season Structure

Short-Run Dominance: The vast majority of Netflix TV shows are limited series or run for only 1 to 2 seasons (median number of seasons across almost all genres is 1–2).

Long-Form Outliers: Classic & Cult TV is a major outlier, averaging over 4.5 seasons (and stretching up to 8+ median seasons), indicating that older television formats licensed by Netflix tended to have much longer syndicated runs than modern Netflix Originals.

## 11. Title Text Analytics (Character & Word Counts)

Optimal Title Length: Title character lengths follow a right-skewed distribution, with most titles peaking around 10 to 20 characters (typically 2 to 3 words).

Type Consistency: Both Movies and TV Shows share an almost identical distribution for title length, with a median of roughly 15 characters. However, Movies feature a higher upper-bound of extreme outliers (some titles exceeding 100 characters).

## 12. Title Length Evolution Over Time

Gradual Increase in Title Length: Looking at average content title length by release year, titles produced in recent years (2010–2021) show a steady upward drift, increasing from an average of ~16 characters up to nearly 19 characters.
