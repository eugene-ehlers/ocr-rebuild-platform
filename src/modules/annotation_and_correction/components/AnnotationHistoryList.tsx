import React from "react";
import { AnnotationRecord } from "../types";

interface AnnotationHistoryListProps {
  items: AnnotationRecord[];
}

export function AnnotationHistoryList({ items }: AnnotationHistoryListProps) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.annotationId}>
          {item.fieldReference} - {item.reviewerStatus}
        </li>
      ))}
    </ul>
  );
}
