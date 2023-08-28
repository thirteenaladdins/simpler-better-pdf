import React from 'react';
import ListItem from '../components/ListItem';

export default function ListFiles(state) {
  const items = [...state.selectedFiles].map((file) => (
    // FIXME: it's unlikely that the user will have the same file twice
    // but should I change this just in case?
    <ListItem key={file.name} fileName={file.name} />
  ));
  return items;
}
