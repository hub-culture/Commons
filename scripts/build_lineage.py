"""Build the first-pass map of Elinor Ostrom's academic lineage.

Source: Jagger, P. (ed.), "Artisans of Political Theory and Empirical Inquiry",
Vincent and Elinor Ostrom Workshop in Political Theory and Policy Analysis,
Indiana University (c. 2009-10):
https://ostromworkshop.indiana.edu/pdf/ArtisansOfPoliticalTheory_Jagger.pdf
  - Appendix A: Dissertations Completed at Indiana University
    (Supervised by Workshop Faculty)
  - Appendix B: External Workshop-Affiliated Faculty
  - Appendix C: Indiana University Workshop-Affiliated Faculty

Tiers follow the "gradient of heirs" idea from the COP31 conversation. They are
labels for a first pass, not computed probabilities:
  T1  Workshop PhD on commons, natural resources or collective action
  T2  Workshop PhD on other institutional analysis (police, public services ...)
  T3  Workshop-affiliated faculty and close collaborators
  T4  Wider citation network (not yet built; see docs/lineage-method.md)

Run:  python scripts/build_lineage.py
Writes data/lineage/nodes.csv, edges.csv, lineage.json
"""
import csv
import json
import os
import re

SOURCE = "https://ostromworkshop.indiana.edu/pdf/ArtisansOfPoliticalTheory_Jagger.pdf"

# (name, year, topic) from Appendix A
DISSERTATIONS = [
    ("Songmin Ahn", 1995, "governance structure and size of public libraries"),
    ("T. K. Ahn", 2001, "foundations for cooperation in social dilemmas"),
    ("Barbara Allen", 1981, "Tocqueville's political theory and feminist theory"),
    ("David N. Allen", 1980, "street-level police supervision"),
    ("Linda Allen", 2005, "structural choice for the Commission for Environmental Cooperation"),
    ("Krister P. Andersson", 2002, "decentralization and municipal forest governance in Bolivia"),
    ("Eduardo K. Araral", 2006, "irrigation reform in the Philippines"),
    ("John A. Baden", 1969, "social stability among the Hutterites"),
    ("Robert V. Bartlett", 1984, "rationality and science in the National Environmental Policy Act"),
    ("Peter A. Beck", 2000, "participatory conservation in Uganda"),
    ("Michael Berheide", 1984, "Karl Popper and political science methodology"),
    ("Robert L. Bish", 1968, "housing tax and subsidy distribution"),
    ("William Blomquist", 1987, "changing an endangered commons into a managed commons (groundwater)"),
    ("Patrick Brandt", 2001, "agenda setting in executive-congressional relations"),
    ("Brenda K. Bushouse", 1999, "mixed economy of child care"),
    ("Jaesong Choe", 1992, "urban common-property institutions in Seoul"),
    ("Brian K. Collins", 2000, "contestable markets for state economic governance"),
    ("Eric Coleman", 2009, "institutions, trust and collective action"),
    ("James L. Cooper Jr.", 1993, "the Solicitor General and federal litigation"),
    ("Sue E. S. Crawford", 1995, "clergy in the secular city"),
    ("Cynthia Croissant", 2005, "land use and land cover in Monroe County, Indiana"),
    ("Debra L. Dean", 1982, "models of police service production"),
    ("Fabio De Castro", 2000, "fishing accords and political ecology in the Amazon"),
    ("Nives Dolsak", 2000, "marketable permits for the commons"),
    ("Julia Aker Duany", 1996, "Sudanese women and education"),
    ("Wal Duany", 1992, "constitution of order among the Nuer"),
    ("Dean Dudley", 1993, "individual behavior in social dilemmas"),
    ("George Ehrhardt", 2002, "security consultation in Northeast Asia"),
    ("Ginger Elliott-Teague", 2007, "NGOs in policymaking in Tanzania"),
    ("Virginia D. Fielder", 1976, "law enforcement news coverage"),
    ("Michael Fotos III", 1999, "organized interests and environmental policy implementation"),
    ("Celia Futemma", 2000, "property rights to natural resources in the Lower Amazon"),
    ("David Goetze", 1980, "state air pollution control agencies"),
    ("Barbara P. Greene", 1971, "responsiveness and control in regulation"),
    ("Vernon L. Greene", 1978, "metaphysical foundations of constitutional order"),
    ("Phillip M. Gregg", 1972, "reformulating theory in policy studies"),
    ("Nathan Griffith", 2004, "constitutional economics of regional integration"),
    ("Patrick J. Haney", 1992, "organizing for foreign policy and crisis decision-making"),
    ("Tanya Hayes", 2007, "forest governance in the Mosquitia corridor, Honduras and Nicaragua"),
    ("Andrew R. Herr", 1996, "appropriation externalities in the commons"),
    ("Chi-Kan Richard Hung", 1999, "credit risk and rules in microcredit"),
    ("Su-Ik Hwang", 1985, "constitutional choice and the individual calculus of voting"),
    ("Pamela Jagger", 2009, "forest sector devolution and rural livelihoods in western Uganda"),
    ("Avra Johnson", 2001, "community development corporations in Indianapolis"),
    ("Derek Kauneckis", 2005, "co-production of property rights in southern Mexico"),
    ("David A. Kessler", 1989, "neighborhood-oriented policing and officers' attitudes"),
    ("Tomas M. Koontz", 1997, "federalism and natural resource policy"),
    ("Wai Fung Lam", 1994, "irrigation systems in Nepal"),
    ("Myungsuk Lee", 1994, "institutional analysis and collective action in common-pool resources"),
    ("Brian Loveman", 1973, "agrarian reform in Chile"),
    ("Anthony P. Matejczyk", 1997, "institutionally induced consensus and zoning exceptions"),
    ("James C. McDavid", 1975, "interjurisdictional cooperation and police performance in St. Louis"),
    ("John P. McIver", 1986, "control of bureaucrats and urban policing"),
    ("Esther Mwangi", 2003, "property rights transformation in Kenya's Maasailand"),
    ("Marissa Myers", 1997, "(topic not captured)"),
    ("Tun Myint", 2005, "multilayer environmental governance in the Mekong and Rhine river basins"),
    ("Evelyn Lwanga Namubiru", 2008, "coping with top-down institutional change in forestry"),
    ("Brent Never", 2005, "institution making in times of crisis (Benin)"),
    ("Matthew Potoski", 1998, "air pollution regulation in the American states"),
    ("Aseem Prakash", 1997, "corporate environmentalism beyond compliance"),
    ("Susan Raines", 2002, "stakeholder absence in international environmental agreements (ISO 14001)"),
    ("Dixie Wiles Ray", 1992, "neighborhood health centers and collective action"),
    ("Ashok Regmi", 2007, "group heterogeneity and collective action in irrigation and forests, Nepal"),
    ("Derek Reiners", 2006, "public land agencies and wildfire in the Interior West"),
    ("Michael E. Roberts", 2008, "human collective behavior"),
    ("Daniel M. Sabet", 2005, "nonprofits and water and sanitation on Mexico's northern border"),
    ("Filippo Sabetti", 1977, "the political basis of human misery in a Sicilian village"),
    ("Jeanne Schaaf", 1989, "competitive entry into telecommunications markets"),
    ("Edella Schlager", 1990, "governance of coastal fisheries"),
    ("Michael Schoon", 2008, "robustness and governance in southern African peace parks"),
    ("Charles M. Schweik", 1998, "spatial and temporal analysis of forest resources and institutions"),
    ("Brian Shoup", 2007, "institutional incentives and interethnic conflict"),
    ("Maria Clara Silva-Forsberg", 1999, "protecting an urban forest reserve in the Amazon"),
    ("John Sislin", 1993, "military assistance and political compliance"),
    ("Dennis C. Smith", 1976, "police professionalization and performance"),
    ("Ronald S. Smith", 2006, "social capital and neighborhood associations"),
    ("Jane Southworth", 2000, "climate change and land cover change impacts on ecosystems"),
    ("Mark Sproule-Jones", 1970, "a theory of public employment"),
    ("Michael Leslie Squires", 1982, "modeling the US-USSR strategic arms race"),
    ("Wenjie Sun", 2006, "land-use and land-cover change in south-central Indiana"),
    ("David W. Swindell", 1997, "community organizations in Indianapolis neighborhoods"),
    ("Shui Yan Tang", 1989, "institutions and collective action in irrigation systems"),
    ("James T. Thomson", 1976, "law and rural institutions in Hausa-speaking Niger"),
    ("Maria Angelica Toniolo", 2004, "land tenure and accidental fires in the Amazon"),
    ("Jennifer Turner", 1997, "local government entrepreneurship in the Chinese water sector"),
    ("Paul W. Turner", 1998, "constitutional orders and deforestation in the humid tropics"),
    ("Frank van Laerhoven", 2008, "local governance and collective action dilemmas"),
    ("Douglas E. Van Houweling", 1976, "a microeconomic theory of political participation"),
    ("George Varughese", 1999, "villagers, bureaucrats and forests in Nepal"),
    ("Nathan Vogt", 2005, "institutions and land-cover change in Uganda"),
    ("S. Tjip Walker", 1998, "the political economy of privatization in Africa"),
    ("Jianxun Wang", 2006, "village governance in contemporary China"),
    ("David Welch", 2007, "forest dynamics in south-central Indiana and southern Illinois"),
    ("Gordon P. Whitaker", 1971, "urban police forces and neighborhood services"),
    ("Richard K. Wilson", 1982, "institutional effects on committee behavior (experiment)"),
    ("Lois R. Wise", 1982, "public employee membership incentives"),
    ("James S. Wunsch", 1974, "voluntary associations in Ghanaian secondary cities"),
    ("Susan G. Wynne", 1989, "the land boards of Botswana"),
    ("Tracy Yandle", 2001, "individual tradable quotas in New Zealand fisheries"),
    ("Tai-Shuenn Yang", 1987, "property rights and constitutional order in imperial China"),
    ("Abigail York", 2005, "land use institutions in an urbanizing landscape"),
    ("Donald G. Zauderer", 1971, "political consequences of the Ohio ballot form"),
]

# (name, affiliation) from Appendices B and C
AFFILIATED = [
    ("Arun Agrawal", "University of Michigan"),
    ("Paul Aligica", "Mercatus Center, George Mason University"),
    ("J. Marty Anderies", "Arizona State University"),
    ("Xavier Basurto", "Duke University Marine Laboratory"),
    ("Kenneth Bickers", "University of Colorado Boulder"),
    ("Juan-Camilo Cardenas", "Universidad de Los Andes, Bogota"),
    ("Salvador Espinosa", "San Diego State University"),
    ("Clark Gibson", "University of California, San Diego"),
    ("Charlotte Hess", "Syracuse University (former Workshop librarian; Digital Library of the Commons)"),
    ("Marco Janssen", "Arizona State University"),
    ("In Kim", "Pusan National University"),
    ("Kwanbo Kim", "The Catholic University of Korea"),
    ("Maria Claudia Lopez", "Pontificia Universidad Javeriana, Bogota"),
    ("Thomas Lyon", "University of Michigan"),
    ("Jennifer McKay", "University of South Australia"),
    ("Amy Poteete", "Concordia University, Montreal"),
    ("Larry Schroeder", "Syracuse University"),
    ("Emil Uddhammar", "Vaxjo University"),
    ("Jon Unruh", "McGill University"),
    ("Tommaso Vitale", "Universita di Milano Bicocca"),
    ("Matthew Auer", "Indiana University"),
    ("Stephen Benard", "Indiana University"),
    ("William Bianco", "Indiana University"),
    ("Lisa Blomgren Bingham", "Indiana University"),
    ("Eileen Braman", "Indiana University"),
    ("Jerome Busemeyer", "Indiana University"),
    ("Daniel Cole", "Indiana University School of Law"),
    ("Aurelian Craiutu", "Indiana University"),
    ("Tom Evans", "Indiana University (CIPEC)"),
    ("Burnell Fischer", "Indiana University"),
    ("Roy Gardner", "Indiana University (Economics)"),
    ("Kerry Krutilla", "Indiana University"),
    ("Lauren Morris MacLean", "Indiana University"),
    ("John Maxwell", "Indiana University"),
    ("Michael McGinnis", "Indiana University (Workshop co-director)"),
    ("Lloyd Orr", "Indiana University"),
    ("Roger Parks", "Indiana University"),
    ("Eric Rasmusen", "Indiana University"),
    ("Armando Razo", "Indiana University"),
    ("Kenneth Richards", "Indiana University"),
    ("Amos Sawyer", "Indiana University (Workshop)"),
    ("Beate Sissenich", "Indiana University"),
    ("Regina Smyth", "Indiana University"),
    ("Jeffrey Stake", "Indiana University School of Law"),
    ("Verlon Stone", "Indiana University"),
    ("Catherine Tucker", "Indiana University (Anthropology)"),
    ("James Walker", "Indiana University (Workshop co-director)"),
]

COMMONS_TERMS = re.compile(
    r"commons|common-pool|common-property|fisher|forest|irrigation|water|"
    r"groundwater|land|property rights|resource|environment|amazon|"
    r"collective action|social dilemma|cooperation|peace parks|quota|permit|"
    r"deforestation|wildfire|conservation|climate|tenure|air pollution|river|"
    r"agrarian|collective behav",
    re.I,
)

THEMES = [
    ("Forests", r"forest|deforestation|wildfire|land cover|land-cover|land use|land-use"),
    ("Water and irrigation", r"irrigation|water|groundwater|river"),
    ("Fisheries and oceans", r"fisher|fishing|quota"),
    ("Land and property rights", r"property rights|tenure|land boards|agrarian|common-property|maasailand"),
    ("Collective action and experiments", r"collective action|social dilemma|cooperation|collective behavior|experiment"),
    ("Environmental policy", r"environment|pollution|conservation|climate|permit|peace parks|nepa|national environmental"),
    ("Public services and policing", r"police|policing|law enforcement|public employ|librar|child care|health|community|neighborhood|zoning"),
    ("Constitutional and political theory", r"constitution|tocqueville|popper|theory|voting|participation|order"),
]


def theme_for(topic):
    for label, pattern in THEMES:
        if re.search(pattern, topic, re.I):
            return label
    return "Other institutional analysis"


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main():
    out = os.path.join("data", "lineage")
    os.makedirs(out, exist_ok=True)
    nodes = [
        {"id": "elinor-ostrom", "name": "Elinor Ostrom", "tier": "T0", "role": "root",
         "year": 1965, "detail": "Political scientist; 2009 Nobel in economics; co-founded the Workshop with Vincent Ostrom (1973)",
         "theme": "Root", "source": SOURCE},
        {"id": "vincent-ostrom", "name": "Vincent Ostrom", "tier": "T0", "role": "co-founder",
         "year": None, "detail": "Founding director of the Workshop; Elinor Ostrom's mentor and spouse",
         "theme": "Root", "source": SOURCE},
    ]
    edges = [{"source": "vincent-ostrom", "target": "elinor-ostrom", "type": "co-founder"}]

    for name, year, topic in DISSERTATIONS:
        tier = "T1" if COMMONS_TERMS.search(topic) else "T2"
        nid = slug(name)
        nodes.append({"id": nid, "name": name, "tier": tier, "role": "workshop-phd",
                      "year": year, "detail": topic, "theme": theme_for(topic), "source": SOURCE})
        edges.append({"source": "elinor-ostrom", "target": nid, "type": "workshop-phd"})

    phd_ids = {n["id"] for n in nodes}
    for name, aff in AFFILIATED:
        nid = slug(name)
        if nid in phd_ids:
            # already a Workshop PhD; record the later affiliation
            for n in nodes:
                if n["id"] == nid:
                    n["later_affiliation"] = aff
            continue
        nodes.append({"id": nid, "name": name, "tier": "T3", "role": "affiliated-faculty",
                      "year": None, "detail": aff, "theme": "Affiliated faculty", "source": SOURCE})
        edges.append({"source": "elinor-ostrom", "target": nid, "type": "affiliated"})

    with open(os.path.join(out, "nodes.csv"), "w", newline="") as f:
        cols = ["id", "name", "tier", "role", "year", "theme", "detail", "later_affiliation", "source"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for n in nodes:
            w.writerow({c: n.get(c, "") for c in cols})
    with open(os.path.join(out, "edges.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source", "target", "type"])
        w.writeheader()
        w.writerows(edges)

    tiers = {}
    for n in nodes:
        tiers[n["tier"]] = tiers.get(n["tier"], 0) + 1
    themes = {}
    for n in nodes:
        if n["role"] == "workshop-phd":
            themes[n["theme"]] = themes.get(n["theme"], 0) + 1
    meta = {
        "title": "Library of the Commons: Ostrom lineage, first pass",
        "version": "0.1.0",
        "source": SOURCE,
        "notes": [
            "Generation 1 only. Appendix A lists dissertations supervised by Workshop faculty, not only by Elinor Ostrom personally.",
            "Snapshot as of the source document (c. 2009-10). Later PhDs and later generations are not yet included.",
            "Tiers are labels for a first pass, not probabilities.",
        ],
        "counts": {"tiers": tiers, "workshop_phd_themes": themes},
        "nodes": nodes,
        "edges": edges,
    }
    with open(os.path.join(out, "lineage.json"), "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    print(json.dumps(meta["counts"], indent=2))


if __name__ == "__main__":
    main()
