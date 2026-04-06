import os
import json
from pydantic import ValidationError
from agents.market_analyst import market_analyst_agent
from agents.product_manager import product_manager_agent
from agents.financial_analyst import financial_analyst_agent, FinancialStrategy
from agents.pitch_creater import pitch_creator_agent

_PIPELINE_CACHE_FILES = ("market_cache.txt", "product_cache.txt", "finance_cache.txt")


def clear_pipeline_caches() -> None:
    """Remove step caches so the next run regenerates market → product → finance."""
    for fname in _PIPELINE_CACHE_FILES:
        if os.path.isfile(fname):
            try:
                os.remove(fname)
            except OSError:
                pass
    print("   -> 🗑️  Cleared pipeline caches (market, product, finance).")


def run_startup_pipeline(user_idea: str, clarification: str | None = None):
    if clarification:
        full_query = f"Idea: {user_idea}\nUser Clarification: {clarification}"
        print("🚀 Resuming pipeline with clarification...\n")
    else:
        full_query = user_idea
        print("🚀 Starting AI Startup-in-a-Box...\n")

    # --- Step 1: Market Analysis ---
    print("🕵️  1. Market Analyst is researching...")
    if os.path.exists("market_cache.txt"):
        print("   -> 📦 Loading Market Report from cache...")
        with open("market_cache.txt", "r", encoding="utf-8") as f:
            market_report = f.read()
    else:
        print("   -> 🧠 Generating new Market Report...")
        market_report = market_analyst_agent.run(full_query)

        if "?" in str(market_report)[-20:]:
            return {"status": "paused", "data": str(market_report)}

        with open("market_cache.txt", "w", encoding="utf-8") as f:
            f.write(str(market_report))

    # --- Step 2: Product Management ---
    print("\n👔  2. Product Manager is extracting features...")
    if os.path.exists("product_cache.txt"):
        print("   -> 📦 Loading Product Spec from cache...")
        with open("product_cache.txt", "r", encoding="utf-8") as f:
            product_spec = f.read()
    else:
        print("   -> 🧠 Generating new Product Spec...")
        product_spec = product_manager_agent.run(market_report)
        with open("product_cache.txt", "w", encoding="utf-8") as f:
            f.write(str(product_spec))

    # --- Step 3: Financial Analysis ---
    print("\n📊  3. Financial Analyst is building the business model...")
    if os.path.exists("finance_cache.txt"):
        print("   -> 📦 Loading Financial Strategy from cache...")
        with open("finance_cache.txt", "r", encoding="utf-8") as f:
            raw_finance = f.read()
    else:
        print("   -> 🧠 Generating new Financial Strategy...")
        finance_context = f"Market Data:\n{market_report}\n\nProduct Data:\n{product_spec}"
        raw_finance = financial_analyst_agent.run(finance_context)
        with open("finance_cache.txt", "w", encoding="utf-8") as f:
            f.write(str(raw_finance))

    try:
        finance_json = json.loads(str(raw_finance))
        validated_finance = FinancialStrategy(**finance_json)
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"❌ Financial parsing failed. The agent returned malformed data: {e}")
        return {"status": "error", "data": f"Financial parsing failed: {e}"}

    # --- Step 4: Pitch Deck Creation ---
    print("\n🎨  4. Pitch Creator is designing the deck...")
    final_context = f"""
    Market Report: {market_report}
    Product Spec: {product_spec}
    Financial Strategy: {validated_finance.model_dump_json(indent=2)}
    """

    pitch_deck_markdown = pitch_creator_agent.run(final_context)

    with open("final_pitch_deck.md", "w", encoding="utf-8") as f:
        f.write(str(pitch_deck_markdown))

    clear_pipeline_caches()

    print("\n✅ Success! Pitch deck saved to 'final_pitch_deck.md'")

    return {"status": "success", "data": str(pitch_deck_markdown)}


def main() -> None:
    """Console entry point for `startup-pipeline` (see pyproject.toml)."""
    result = run_startup_pipeline("A quiz for UPSC Aspirants based on daily news articles.")
    if isinstance(result, dict):
        status = result.get("status")
        if status == "paused":
            print("\n--- Pipeline paused (needs clarification) ---\n", result.get("data"))
        elif status == "error":
            print("\n--- Pipeline error ---\n", result.get("data"))


if __name__ == "__main__":
    main()
