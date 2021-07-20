export interface Page {
  key: number;
  text: string;
  name: string;
  type: string;
  data: Array<Object>;
}

export interface Report {
  key: number;
  text: string;
  name: string;
  type: string;
  data: Array<Object>;
  headers: Array<Object>;
}

export interface IAbcLicCheckState {
  currentPage: Page;
  menuOptions: Array<Page>;
  reports: Array<Page>;
}