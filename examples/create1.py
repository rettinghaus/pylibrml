import json
from datetime import date

from model.librml import LibRML, Action, ActionType, Restriction, RestrictionType

if __name__ == '__main__':
    id = 'id-123456'
    # create empty LibRML-Object with a id
    librml = LibRML(itemid=id)

    # set some attributes
    librml.tenant = 'https://www.slub-dresden.de/'
    librml.sharealike = True
    librml.mention = True
    librml.copyright = True
    librml.commercialuse = False

    print('Output after creation and setting some attributes:')
    print(json.dumps(librml.to_dict(), indent=4))

    # Add a action and a restriction
    librml.actions.append(
        Action(
            type=ActionType.READ,
            permission=True,
            restrictions=[
                Restriction(
                    res_type=RestrictionType.DATE,
                    fromdate=date(year=2026, month=2, day=11)),
                Restriction(
                    res_type=RestrictionType.QUALITY,
                    maxdimension=1080)
            ],
        )
    )

    print('Output after a action with a restriction:')
    print(json.dumps(librml.to_dict(), indent=4))

    # The same works with a json
    download_restriction: str = json.dumps({
        "type": "download",
        "permission": True,
        "restrictions": [
            {
                "type": "date",
                "fromdate": "2026-02-11"
            }
        ]
    })
    action_from_json = Action.from_jsonstr(download_restriction)
    librml.actions.append(action_from_json)

    print('Output after added json:')
    print(json.dumps(librml.to_dict(), indent=4))

    # Same with a XML
    print_restriction: str = '''
        <action type="print" permission="true">
            <restriction type="date" fromdate="2026-02-11" />
        </action>
        '''

    action_from_xml = Action.from_xmlstr(print_restriction)
    librml.actions.append((action_from_xml))

    print('Output after added xml:')
    print(json.dumps(librml.to_dict(), indent=4))

    # Load a LibRML from the JSON-String created above

    librml_json_str = json.dumps(librml.to_dict())

    librm2 = LibRML.from_jsonstr(librml_json_str)

    # Now, let's get some infos out of this LibRML

    print('All actions: {}'.format(librml.allactionnames()))
    print('XML Output:')
    print(librml.to_xml())

    # Test agreement restriction
    agreement_action = Action(
        type=ActionType.DOWNLOAD,
        permission=True,
        restrictions=[
            Restriction(res_type=RestrictionType.AGREEMENT, required=True)
        ]
    )
    librml.actions.append(agreement_action)
    print('Output after adding agreement action:')
    print(json.dumps(librml.to_dict(), indent=4))
