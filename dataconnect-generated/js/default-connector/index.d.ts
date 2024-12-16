import { ConnectorConfig, DataConnect } from 'firebase/data-connect';
export const connectorConfig: ConnectorConfig;

export type TimestampString = string;

export type UUIDString = string;

export type Int64String = string;

export type DateString = string;



export interface Category_Key {
  id: string;
  __typename?: 'Category_Key';
}

export interface Collection_Key {
  id: string;
  __typename?: 'Collection_Key';
}

export interface Product_Key {
  id: string;
  __typename?: 'Product_Key';
}

export interface Subcategory_Key {
  id: string;
  __typename?: 'Subcategory_Key';
}

export interface Subcollection_Key {
  id: string;
  __typename?: 'Subcollection_Key';
}

export interface User_Key {
  id: string;
  __typename?: 'User_Key';
}



