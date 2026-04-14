"""
Rumor detection ML model using TF-IDF + Logistic Regression.

The model is trained on a small set of labeled examples to distinguish
rumor-style text from factual-style text.  It is intentionally lightweight
so that the application starts quickly without any external model files.
"""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# ---------------------------------------------------------------------------
# Training corpus
# ---------------------------------------------------------------------------
# Each entry is (text, label) where label 1 = rumor, 0 = not a rumor.
# The examples cover common linguistic patterns found in misinformation
# research (vague attribution, sensational claims, forwarded-message
# language) versus factual, source-attributed reporting.
_TRAINING_DATA: list[tuple[str, int]] = [
    # --- Rumors (label = 1) ---
    ("BREAKING: Scientists discover that drinking coffee causes instant blindness, share before deleted!", 1),
    ("A friend told me the government is secretly adding chemicals to tap water to control people's minds.", 1),
    ("URGENT: Forward this message – Bill Gates confirmed that the new vaccine contains microchips!", 1),
    ("They don't want you to know this but 5G towers are spreading the disease, spread the word!", 1),
    ("Shocking truth revealed: the moon landing was filmed in Hollywood by Stanley Kubrick!", 1),
    ("Doctors are hiding the cure for cancer because Big Pharma pays them to keep people sick.", 1),
    ("SHARE IMMEDIATELY: Eating bananas every day will kill you within a week according to secret study.", 1),
    ("A source inside the White House says the president is planning to suspend elections next year.", 1),
    ("Scientists confirmed the Earth is flat; NASA has been lying to us for decades!", 1),
    ("This photo proves that aliens built the pyramids – mainstream media is covering it up.", 1),
    ("I heard from a reliable insider that the stock market will completely crash tomorrow!", 1),
    ("Secret memo leaked: water fluoridation is actually a mind-control experiment run by the CIA.", 1),
    ("Warning: new law will allow police to enter your home without a warrant starting next month!", 1),
    ("Unbelievable: local man cures stage-4 cancer in 3 days using this one weird trick doctors hate.", 1),
    ("They are putting tracking devices in dollar bills – check yours now!", 1),
    ("Breaking news that mainstream media won't show you: celebrity fakes death to avoid taxes.", 1),
    ("Rumor has it that the new smartphone update is designed to spy on all your conversations.", 1),
    ("Sources say the army has been deploying secret weapons against civilians for years.", 1),
    ("This leaked document shows that vaccines are 100% causing autism in children.", 1),
    ("I can't believe no one is talking about this – chemtrails are poisoning our food supply!", 1),
    ("Insider tip: the entire cryptocurrency market is a government ponzi scheme about to collapse.", 1),
    ("They want to ban this natural remedy because it cures everything and costs nothing.", 1),
    ("A whistleblower just revealed that hospitals are paid to inflate COVID death counts.", 1),
    ("MUST READ: Scientists have found definitive proof that climate change is a hoax.", 1),
    ("Share before it's removed: new evidence proves that the 2020 election was stolen.", 1),

    # --- Not rumors (label = 0) ---
    ("According to a peer-reviewed study published in Nature, regular exercise reduces heart disease risk by 30%.", 0),
    ("The World Health Organization confirmed in its official report that hand washing prevents the spread of many infections.", 0),
    ("NASA released new high-resolution images of Mars captured by the Perseverance rover.", 0),
    ("The Federal Reserve announced a 0.25% interest rate increase at its quarterly meeting today.", 0),
    ("Researchers at MIT developed a new battery technology that could double the range of electric vehicles.", 0),
    ("The United Nations climate report states that global temperatures have risen 1.1°C since pre-industrial times.", 0),
    ("Apple reported quarterly earnings of $89.5 billion, exceeding analyst expectations.", 0),
    ("A clinical trial involving 40,000 participants showed the new drug reduces tumor growth in 60% of cases.", 0),
    ("The European Central Bank raised its benchmark interest rate to combat rising inflation.", 0),
    ("Scientists identified a new species of deep-sea fish near hydrothermal vents in the Pacific Ocean.", 0),
    ("The Supreme Court ruled 6-3 on the landmark privacy case, citing the Fourth Amendment.", 0),
    ("SpaceX successfully launched 60 Starlink satellites into low Earth orbit on Thursday.", 0),
    ("The National Weather Service issued a winter storm warning for the northeastern United States.", 0),
    ("A study in The Lancet found that air pollution contributes to approximately 7 million deaths per year globally.", 0),
    ("The city council voted 8-2 to approve the new public transit expansion project.", 0),
    ("According to the Bureau of Labor Statistics, the unemployment rate fell to 3.7% last month.", 0),
    ("The International Monetary Fund projects global GDP growth of 3.2% for the current fiscal year.", 0),
    ("Archaeologists uncovered a 3,000-year-old settlement near the banks of the Nile River.", 0),
    ("The Centers for Disease Control reports that flu vaccination reduces hospitalization risk by 40%.", 0),
    ("Engineers at CERN detected new particle interactions consistent with the Standard Model predictions.", 0),
    ("The World Bank released data showing global poverty fell by 2% in the last decade.", 0),
    ("A new study from Stanford University links sleep deprivation to increased cardiovascular risk.", 0),
    ("The Department of Transportation published its annual highway safety report with updated statistics.", 0),
    ("Meteorologists predict above-average rainfall in California this winter due to La Niña conditions.", 0),
    ("The European Space Agency confirmed the launch date for its Jupiter Icy Moons Explorer mission.", 0),
]

_TEXTS = [t for t, _ in _TRAINING_DATA]
_LABELS = [l for _, l in _TRAINING_DATA]

# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def _build_pipeline() -> Pipeline:
    """Build and train the rumor-detection pipeline."""
    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    max_features=5000,
                    sublinear_tf=True,
                    min_df=1,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    C=1.0,
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )
    pipeline.fit(_TEXTS, _LABELS)
    return pipeline


# Module-level singleton – trained once on import.
_pipeline: Pipeline = _build_pipeline()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def predict(text: str) -> dict:
    """Return a prediction dict for the given *text*.

    Returns
    -------
    dict with keys:
        label   – "rumor" | "not_rumor"
        confidence – float in [0, 1] representing model certainty
        rumor_probability – float in [0, 1]
    """
    proba = _pipeline.predict_proba([text])[0]
    # Index 0 = not_rumor (class 0), index 1 = rumor (class 1)
    rumor_prob = float(proba[1])
    label = "rumor" if rumor_prob >= 0.5 else "not_rumor"
    confidence = float(max(proba))
    return {
        "label": label,
        "confidence": round(confidence, 4),
        "rumor_probability": round(rumor_prob, 4),
    }
