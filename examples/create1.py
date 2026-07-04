import json
from datetime import date

from model.librml import LibRML, Action, ActionType, Restriction, RestrictionType

if __name__ == '__main__':
    item_id = 'id-123456'
    # create empty LibRML-Object with an id
    librml = LibRML(itemid=item_id)

    # set some attributes
    librml.tenant = 'https://www.slub-dresden.de/'
    librml.sharealike = True
    librml.mention = True
    librml.copyright = True
    librml.commercialuse = False

    print('Output after creation and setting some attributes:')
    print(json.dumps(librml.to_dict(), indent=4))

    # Add an action and restrictions
    librml.actions.append(
        Action(
            type=ActionType.READ,
            permission=True,
            restrictions=[
                Restriction(
                    res_type=RestrictionType.DATE,
                    fromdate=date(year=2026, month=2, day=11)
                ),
                Restriction(
                    res_type=RestrictionType.QUALITY,
                    maxdimension=1080
                )
            ]
        )
    )

    # Add another action with an agreement requirement
    librml.actions.append(
        Action(
            type=ActionType.DOWNLOAD,
            permission=True,
            restrictions=[
                Restriction(
                    res_type=RestrictionType.AGREEMENT,
                    required=True
                )
            ]
        )
    )

    print('\nOutput after adding actions with restrictions:')
    print(json.dumps(librml.to_dict(), indent=4))

    # Output as XML
    print('\nOutput as XML:')
    print(librml.to_xml())

    # Load a LibRML from the JSON-String created above
    librml_json_str = json.dumps(librml.to_dict())
    librml2 = LibRML.from_jsonstr(librml_json_str)

    print('\nOutput after reread from JSON:')
    print(json.dumps(librml2.to_dict(), indent=4))

    # Input from XML
    librml3 = LibRML.from_xmlstr(xmlstr=librml.to_xml())

    print('\nOutput after reread from XML:')
    print(json.dumps(librml3.to_dict(), indent=4))
