import Analysis.gpt_source as gpt
import Analysis.analyzer as anl

if __name__ == "__main__":

    print("Loading DB")

    names_db: anl.NamesDataBase = anl.NamesDataBase(
        "./data-bases/names_surnames.csv"
    )

    print("Analysier init")

    analysier: anl.Analysier = anl.Analysier(
        "CHAT_NAME",
        names_db,
        gpt.Chat(
            gpt.models_stock.gpt_4o_mini,
            gpt.provider_stock.PollinationsAI
        )
    )

    print("Loading detected info")
    analysier.load_info()

    print("Performing analysis")
    reports = analysier.analysie_all()

    print("Reports generated")
    for (person, report) in reports:
        print(report)
        print()