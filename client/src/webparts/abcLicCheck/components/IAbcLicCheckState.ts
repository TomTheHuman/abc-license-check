export interface Page {
  key: number;
  text: string;
  name: string;
  type: string;
  data: Array<any>;
}

export interface IAbcLicCheckState {
  currentPage: Page;
  menuOptions: Array<Page>;
  reports: Array<Page>;
}