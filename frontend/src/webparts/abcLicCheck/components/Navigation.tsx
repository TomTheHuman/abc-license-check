import * as React from 'react';
import styles from './AbcLicCheck.module.scss';
import { IAbcLicCheckProps } from './IAbcLicCheckProps';
import { escape } from '@microsoft/sp-lodash-subset';
import { PropertyPaneSlider } from '@microsoft/sp-property-pane';

const Navigation = ({ handlePageButton, state }) => {

  return (
      <div className={ styles.nav }>
        <div className={ styles.pageButtons }>
            <button 
                onClick={() => handlePageButton('dashboard')} 
                id={state.currentPage == 'dashboard' ? styles.selectedPage : ''} 
                className={ styles.pageButton }>
                    Dashboard
            </button>
            { GetPageButtons(handlePageButton, state) }
            { console.log(state.reports) }
        </div>
        <div className={ styles.optionsButtons }>
            <button id={ styles.optionsButton }>
                ⚙️
            </button>
        </div>
      </div>
    );
};

function GetPageButtons(handlePageButton: Function, state) {
    const buttons = state.reports.map((report) => {
        return(
            <button onClick={() => handlePageButton(report.name)} 
                id={state.currentPage == report.name ? styles.selectedPage : ''} 
                key={report.name.trim()} 
                className={ styles.pageButton }>
                    { report.formalName }
            </button>
        );
    });

    return buttons;
}

export default Navigation;