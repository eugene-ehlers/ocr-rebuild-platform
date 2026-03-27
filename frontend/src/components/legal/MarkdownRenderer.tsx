import ReactMarkdown from 'react-markdown';

type MarkdownRendererProps = {
  content: string;
};

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  return (
    <div className="markdown-renderer">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
}
