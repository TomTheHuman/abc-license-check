import * as React from "react";
import styles from "./AbcLicCheck.module.scss";
import { IAbcLicCheckProps } from "./IAbcLicCheckProps";
import { escape } from "@microsoft/sp-lodash-subset";
import { PropertyPaneSlider } from "@microsoft/sp-property-pane";
import { PrimaryButton } from "office-ui-fabric-react";

// TODO Add logic to hide menus when user clicks anywhere else on page

const Navigation = ({ state, handlePageOption, handlePageButton, handleOptionsButton }) => {
  return (
    <div className={styles.nav}>
      <div className={`${styles.dropDown} ${styles.pageDropDown}`}>
        <button 
        className={`${styles.navButton} ${styles.pageDropBtn}`}
        onClick={() => handlePageButton()}
        >
          Reports
        </button>
        <div 
          className={styles.dropDownContent}
          onClick={handlePageButton}>
          <GetPageOptions state={state} handlePageOption={handlePageOption}/>
        </div>
      </div>
      <div className={styles.pageTitle}>
        <h1 className={styles.pageTitleText}>{state.currentPage.formalName}</h1>
      </div>
      <div className={`${styles.dropDown} ${styles.optDropDown}`}>
        <button 
        className={`${styles.navButton} ${styles.optDropBtn}`}
        onClick={() => handleOptionsButton()}
        >
          Options
        </button>
        <div 
          className={styles.dropDownContent}
          onClick={handleOptionsButton}>
          <GetOptions state={state} handlePageOption={handlePageOption}/>
        </div>
      </div>
    </div>
  );
};

const GetPageOptions = ({state, handlePageOption}) => {

  const buttons = state.pages.map((report) => {
    return (
      <a
        href="#"
        key={report.name.trim()}
        className={styles.dropDownOption}
        onClick={() => handlePageOption(report)}
      >
        {report.formalName}
      </a>
    );
  });

  return state.repMenuOpen && buttons;
}

const GetOptions = ({state, handlePageOption}) => {

  let buttons = state.options.map((option) => {
    return (
      <a
        href="#"
        key={option.name.trim()}
        className={styles.dropDownOption}
        onClick={() => handlePageOption(option)}
      >
        {option.formalName}
      </a>
    );
  });

  return state.optMenuOpen && buttons;
}

export default Navigation;
