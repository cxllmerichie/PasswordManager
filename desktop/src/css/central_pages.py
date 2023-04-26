from ..misc import COLORS


css: str = f'''
#CentralPages {{
    background-image: url(".assets/background.png");
}}
'''

cp_items = f'''
#HintLbl1,
#NoCategoriesLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 20px;
    font-style: italic;
}}

#ItemsScrollArea {{
    background-color: {COLORS.TRANSPARENT};
    border: none;
}}

#ItemsScrollAreaWidget {{
    background-color: {COLORS.TRANSPARENT};
}}

#FavouriteLbl,
#LetterLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 20px;
    font-weight: bold;
}}
'''

cp_item = f'''
#CP_Item {{
    background-color: {COLORS.LIGHT_GRAY};
    border-radius: 10px;
    min-height: 75px;
    max-width: 400px;
}}

#CP_Item:hover {{
    background-color: {COLORS.HOVER};
}}

#ItemTitleLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 22px;
}}

#ItemDescriptionLbl {{
    color: {COLORS.TEXT_SECONDARY};
    font-size: 18px;
}}
'''
