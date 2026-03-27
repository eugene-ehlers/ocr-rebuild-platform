import { LegalDocumentLayout } from '../../components/legal/LegalDocumentLayout';
import { MarkdownRenderer } from '../../components/legal/MarkdownRenderer';
import { LegalDocumentKey, legalDocuments } from '../../content/legal/legalDocuments';

type LegalDocumentPageProps = {
  documentKey: LegalDocumentKey;
};

export function LegalDocumentPage({ documentKey }: LegalDocumentPageProps) {
  const document = legalDocuments[documentKey];

  return (
    <LegalDocumentLayout title={document.title}>
      <MarkdownRenderer content={document.content} />
    </LegalDocumentLayout>
  );
}
