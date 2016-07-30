<%page args="metadata"/>\
<!DOCTYPE html>
<html>
<head>
    <title>${metadata['title']}</title>
    % for k, v in metadata.items():
    <%
        if v == 'title':
            continue
    %>\
<meta name="${k}" content="${v}" />
    % endfor
</head>
<body>
