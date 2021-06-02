import * as React from "react";
import styles from "./AbcLicCheck.module.scss";
import { IAbcLicCheckProps } from "./IAbcLicCheckProps";
import { escape } from "@microsoft/sp-lodash-subset";
import { PropertyPaneSlider } from "@microsoft/sp-property-pane";

const Navigation = ({ handlePageButton, handleOptionButton, state }) => {
  return (
    <div className={styles.nav}>
      <div className={styles.pageButtons}>
        <button
          onClick={() => handlePageButton("dashboard")}
          id={state.currentPage == "dashboard" ? styles.selectedPage : ""}
          className={styles.pageButton}
        >
          Dashboard
        </button>
        {GetPageButtons(handlePageButton, state)}
        {console.log(state.reports)}
      </div>
      <div className={styles.optionsButtons}>
        <button onClick={() => handleOptionButton()} id={styles.optionsButton}>
          ⚙️
        </button>
        {state.menuOpen ? GetOptionMenu(handlePageButton, state) : ""}
      </div>
    </div>
  );
};

function GetPageButtons(handlePageButton: Function, state) {
  const buttons = state.reports.map((report) => {
    return (
      <button
        onClick={() => handlePageButton(report.name)}
        id={state.currentPage == report.name ? styles.selectedPage : ""}
        key={report.name.trim()}
        className={styles.pageButton}
      >
        {report.formalName}
      </button>
    );
  });

  return buttons;
}

function GetOptionMenu(handlePageButton: Function, state) {
  console.log(state);

  function getOptions(options: Array<any>) {
    let optionsHTML = options.map((option) => {
      return (
        <li
          className={styles.optionItem}
          onClick={() => handlePageButton(option.name)}
        >
          {option.formalName}
        </li>
      );
    });

    return optionsHTML;
  }

  return (
    <div className={styles.optionMenu}>
      <ul className={styles.optionList}>{getOptions(state.menuOptions)}</ul>
    </div>
  );
}

export default Navigation;
