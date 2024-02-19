export const convertToHtml = (data, className) => {
	const markup = { __html: data };
	return <div dangerouslySetInnerHTML={markup} className={className} />;
  };