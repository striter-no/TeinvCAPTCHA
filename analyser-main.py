import src.gpt_source as gpt
import src.analyzer as anl

if __name__ == "__main__":

    analysier: anl.Analysier = anl.Analysier(
        "NOBICE_CHAT",
        gpt.Chat(
            gpt.models_stock.gpt_4o_mini,
            gpt.provider_stock.PollinationsAI
        )
    )

    analysier.load_info()

    analysier.analysie_all()