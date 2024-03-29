import * as React from 'react';
import * as ReactDom from 'react-dom';
import { Version } from '@microsoft/sp-core-library';
import {
  IPropertyPaneConfiguration,
  PropertyPaneTextField
} from '@microsoft/sp-property-pane';
import { BaseClientSideWebPart, WebPartContext } from '@microsoft/sp-webpart-base';

import * as strings from 'AbcLicCheckWebPartStrings';
import AbcLicCheck from './components/AbcLicCheck';
import { IAbcLicCheckProps } from './components/IAbcLicCheckProps';

import { initializeIcons } from '@fluentui/font-icons-mdl2';
initializeIcons();

export interface IAbcLicCheckWebPartProps {
  description: string;
  context: WebPartContext;
}

export default class AbcLicCheckWebPart extends BaseClientSideWebPart<IAbcLicCheckWebPartProps> {

  public render(): void {
    const element: React.ReactElement<IAbcLicCheckProps> = React.createElement(
      AbcLicCheck,
      {
        description: this.properties.description,
        context: this.context,
      },
    );

    ReactDom.render(element, this.domElement);
  }

  protected onDispose(): void {
    ReactDom.unmountComponentAtNode(this.domElement);
  }

  protected get dataVersion(): Version {
    return Version.parse('1.0');
  }

  protected getPropertyPaneConfiguration(): IPropertyPaneConfiguration {
    return {
      pages: [
        {
          header: {
            description: strings.PropertyPaneDescription
          },
          groups: [
            {
              groupName: strings.BasicGroupName,
              groupFields: [
                PropertyPaneTextField('description', {
                  label: strings.DescriptionFieldLabel
                })
              ]
            }
          ]
        }
      ]
    };
  }
}
