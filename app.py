"""Netflix EDA dashboard (Streamlit). Run:  streamlit run app.py"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

RED, GREY = "#E50914", "#564D4D"
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
AGE_ORDER = ["New (0-1 yr)", "Recent (2-5 yrs)", "Older (6-10 yrs)", "Catalogue (10+ yrs)"]

# older Streamlit versions don't support width="stretch"
_v = tuple(int(x) for x in st.__version__.split(".")[:2])
STRETCH = {"width": "stretch"} if _v >= (1, 50) else {"use_container_width": True}

st.set_page_config(page_title="Netflix Content Dashboard", page_icon="🎬", layout="wide")


# ---------- data (same cleaning steps as EDA_Netflix.ipynb) ----------
@st.cache_data(show_spinner="Cleaning data…")
def load(src) -> pd.DataFrame:
    df = pd.read_csv(src)
    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), format="%B %d, %Y", errors="coerce")
    df = df.dropna(subset=["date_added"])
    for c in ["description", "cast", "director"]:
        df[c] = df[c].fillna("Unknown")
    df["country"] = df["country"].fillna(df["country"].mode()[0])
    df["rating"] = df["rating"].fillna(df["rating"].mode()[0])
    df["duration"] = df.groupby("type")["duration"].transform(lambda x: x.fillna(x.mode()[0]))
    df = df[~df["rating"].astype(str).str.contains("min")].copy()  # movie length in rating col
    df["duration_num"] = pd.to_numeric(df["duration"].str.split(" ").str[0], errors="coerce")
    df["year_added"] = df["date_added"].dt.year
    df["month_name"] = df["date_added"].dt.month_name()
    df["gap_years"] = (df["year_added"] - df["release_year"]).astype(int)
    df["content_age"] = pd.cut(df["gap_years"], [-999, 1, 5, 10, 999], labels=AGE_ORDER)
    return df


def explode(df, col, n=None):
    """Counts of comma-separated values (cast, director, country, listed_in)."""
    s = (df[col].str.split(",").explode().str.strip().str.lower())
    s = s[(s != "") & (s != "unknown")]
    s = s.value_counts()
    return s.head(n) if n else s


def style(fig, h=380):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=50, b=10),
                      legend_title_text="")
    return fig


def hbar(counts, title, color=RED):
    d = counts.sort_values().reset_index()
    d.columns = ["name", "count"]
    d["name"] = d["name"].str.title()
    fig = px.bar(d, x="count", y="name", orientation="h", title=title,
                 color_discrete_sequence=[color])
    fig.update_layout(yaxis_title="", xaxis_title="Titles")
    return style(fig)


# ---------- sidebar: data + filters ----------
st.sidebar.title("🎬 Netflix EDA")
up = st.sidebar.file_uploader("netflix_titles.csv", type="csv")
local = Path(__file__).parent / "netflix_titles.csv"
if up is not None:
    raw = load(up)
elif local.exists():
    raw = load(local)
else:
    st.title("Netflix Content Dashboard")
    st.info("Upload `netflix_titles.csv` in the sidebar, or place it next to `app.py`.")
    st.stop()

types = st.sidebar.multiselect("Type", sorted(raw["type"].unique()), default=sorted(raw["type"].unique()))
y0, y1 = int(raw["year_added"].min()), int(raw["year_added"].max())
yrs = st.sidebar.slider("Year added", y0, y1, (y0, y1))
ratings = st.sidebar.multiselect("Rating", sorted(raw["rating"].unique()))
countries = st.sidebar.multiselect("Country", list(explode(raw, "country").index[:40]),
                                   format_func=str.title)

df = raw[raw["type"].isin(types) & raw["year_added"].between(*yrs)]
if ratings:
    df = df[df["rating"].isin(ratings)]
if countries:
    pat = "|".join(countries)
    df = df[df["country"].str.lower().str.contains(pat, regex=True)]
if df.empty:
    st.warning("No titles match the current filters.")
    st.stop()

# ---------- header + KPIs ----------
st.title("Netflix Content Dashboard")
st.caption("Interactive version of the EDA notebook. Use the sidebar to filter every chart.")

movies, shows = df[df["type"] == "Movie"], df[df["type"] == "TV Show"]
k = st.columns(5)
k[0].metric("Titles", f"{len(df):,}")
k[1].metric("Movies", f"{len(movies):,}")
k[2].metric("TV shows", f"{len(shows):,}")
k[3].metric("Median movie length", f"{movies['duration_num'].median():.0f} min" if len(movies) else "–")
k[4].metric("Median seasons", f"{shows['duration_num'].median():.0f}" if len(shows) else "–")

t1, t2, t3, t4, t5 = st.tabs(["Overview", "Growth & timing", "Genres & countries", "People", "Ratings & duration"])

# ---------- Overview ----------
with t1:
    c1, c2 = st.columns([1, 2])
    tc = df["type"].value_counts().reset_index()
    fig = px.pie(tc, names="type", values="count", hole=0.55, title="Movies vs TV shows",
                 color="type", color_discrete_map={"Movie": RED, "TV Show": GREY})
    c1.plotly_chart(style(fig), **STRETCH)
    ry = df.groupby("release_year").size().reset_index(name="count")
    fig = px.bar(ry, x="release_year", y="count", title="Titles by release year",
                 color_discrete_sequence=[RED])
    c2.plotly_chart(style(fig), **STRETCH)

# ---------- Growth & timing ----------
with t2:
    c1, c2 = st.columns(2)
    yr = df.groupby("year_added").size()
    fig = px.line(yr.reset_index(name="count"), x="year_added", y="count", markers=True,
                  title="Titles added per year", color_discrete_sequence=[RED])
    c1.plotly_chart(style(fig), **STRETCH)
    g = (yr.pct_change() * 100).dropna()
    if len(g):
        c1.caption(f"Fastest growth year: **{int(g.idxmax())}** (+{g.max():.0f}% vs. previous year)")

    mix = df.groupby(["year_added", "type"]).size().reset_index(name="count")
    mode = c2.radio("Type mix", ["Count", "Share %"], horizontal=True)
    if mode == "Share %":
        mix["count"] = mix["count"] / mix.groupby("year_added")["count"].transform("sum") * 100
    fig = px.bar(mix, x="year_added", y="count", color="type", title="Movies vs TV shows by year added",
                 color_discrete_map={"Movie": RED, "TV Show": GREY})
    c2.plotly_chart(style(fig), **STRETCH)

    c3, c4 = st.columns(2)
    mo = df["month_name"].value_counts().reindex(MONTHS).fillna(0).reset_index()
    mo.columns = ["month", "count"]
    fig = px.bar(mo, x="month", y="count", title="Titles added by month (all years)",
                 color_discrete_sequence=[RED])
    c3.plotly_chart(style(fig), **STRETCH)

    age = df["content_age"].value_counts().reindex(AGE_ORDER).fillna(0).reset_index()
    age.columns = ["age", "count"]
    fig = px.bar(age, x="age", y="count", title="Content age when added (release → Netflix)",
                 color_discrete_sequence=[GREY])
    c4.plotly_chart(style(fig), **STRETCH)

    heat = df.pivot_table(index="year_added", columns=df["date_added"].dt.month,
                          values="show_id", aggfunc="count").fillna(0)
    fig = px.imshow(heat, aspect="auto", color_continuous_scale="Reds", text_auto=".0f",
                    labels=dict(x="Month", y="Year added", color="Titles"),
                    title="Additions heatmap: year × month")
    st.plotly_chart(style(fig, 420), **STRETCH)

# ---------- Genres & countries ----------
with t3:
    n = st.slider("Items to show", 5, 20, 10, key="n1")
    c1, c2 = st.columns(2)
    c1.plotly_chart(hbar(explode(df, "listed_in", n), f"Top {n} genres"), **STRETCH)
    c2.plotly_chart(hbar(explode(df, "country", n), f"Top {n} producing countries", GREY),
                    **STRETCH)

    # country x genre
    cg = df[["show_id", "country", "listed_in"]].copy()
    cg["country"] = cg["country"].str.split(",")
    cg = cg.explode("country", ignore_index=True)
    cg["listed_in"] = cg["listed_in"].str.split(",")
    cg = cg.explode("listed_in", ignore_index=True)
    for c in ["country", "listed_in"]:
        cg[c] = cg[c].str.strip().str.lower()
    cg = cg[(cg["country"] != "") & (cg["country"] != "unknown")]

    st.subheader("Compare two countries")
    avail = list(cg["country"].value_counts().index[:40])
    a, b = st.columns(2)
    ca = a.selectbox("Country A", avail, index=avail.index("india") if "india" in avail else 0, format_func=str.title)
    cb = b.selectbox("Country B", avail, index=avail.index("united states") if "united states" in avail else 1, format_func=str.title)
    cmp_ = cg[cg["country"].isin([ca, cb])]
    top_g = cmp_["listed_in"].value_counts().head(10).index
    d = cmp_[cmp_["listed_in"].isin(top_g)].groupby(["listed_in", "country"]).size().reset_index(name="count")
    d["listed_in"] = d["listed_in"].str.title()
    d["country"] = d["country"].str.title()
    fig = px.bar(d, x="count", y="listed_in", color="country", barmode="group", orientation="h",
                 title=f"Top 10 genres: {ca.title()} vs {cb.title()}",
                 color_discrete_sequence=[RED, GREY],
                 category_orders={"listed_in": [g.title() for g in top_g]})
    fig.update_yaxes(autorange="reversed", title="")
    st.plotly_chart(style(fig, 460), **STRETCH)

    tc8 = cg["country"].value_counts().head(8).index
    tg = cg["listed_in"].value_counts().head(10).index
    sub = cg[cg["country"].isin(tc8) & cg["listed_in"].isin(tg)]
    share = pd.crosstab(sub["country"], sub["listed_in"], normalize="index") * 100
    share.index = share.index.str.title()
    share.columns = share.columns.str.title()
    fig = px.imshow(share.round(0), aspect="auto", color_continuous_scale="Reds", text_auto=".0f",
                    labels=dict(color="% of country"), title="Genre mix by country (% share)")
    st.plotly_chart(style(fig, 440), **STRETCH)

# ---------- People ----------
with t4:
    n2 = st.slider("Items to show", 5, 20, 10, key="n2")
    c1, c2 = st.columns(2)
    c1.plotly_chart(hbar(explode(df, "director", n2), f"Top {n2} directors"), **STRETCH)
    c2.plotly_chart(hbar(explode(df, "cast", n2), f"Top {n2} cast members", GREY), **STRETCH)

# ---------- Ratings & duration ----------
with t5:
    c1, c2 = st.columns(2)
    rt = pd.crosstab(df["rating"], df["type"])
    pct = (rt / rt.sum() * 100).reset_index().melt("rating", var_name="type", value_name="pct")
    order = rt.sum(axis=1).sort_values(ascending=False).index.tolist()
    fig = px.bar(pct, x="rating", y="pct", color="type", barmode="group",
                 title="Rating mix within each type (%)", category_orders={"rating": order},
                 color_discrete_map={"Movie": RED, "TV Show": GREY})
    c1.plotly_chart(style(fig), **STRETCH)

    fig = px.bar(df["rating"].value_counts().reset_index(), x="rating", y="count",
                 title="Titles by rating", color_discrete_sequence=[RED])
    c2.plotly_chart(style(fig), **STRETCH)

    c3, c4 = st.columns(2)
    if len(movies):
        fig = px.histogram(movies, x="duration_num", nbins=40, title="Movie length (minutes)",
                           color_discrete_sequence=[RED])
        c3.plotly_chart(style(fig), **STRETCH)
    if len(shows):
        sc = shows["duration_num"].astype(int).value_counts().sort_index().reset_index()
        fig = px.bar(sc, x="duration_num", y="count", title="TV shows by number of seasons",
                     color_discrete_sequence=[GREY])
        fig.update_xaxes(type="category", title="Seasons")
        c4.plotly_chart(style(fig), **STRETCH)

# ---------- raw data ----------
with st.expander("Browse filtered data"):
    cols = ["title", "type", "director", "country", "date_added", "release_year", "rating", "duration", "listed_in"]
    st.dataframe(df[cols], **STRETCH, hide_index=True)
    st.download_button("Download filtered CSV", df[cols].to_csv(index=False), "netflix_filtered.csv", "text/csv")
