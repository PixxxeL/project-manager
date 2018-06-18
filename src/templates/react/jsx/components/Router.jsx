import React from 'react';


class Router extends React.Component {

    _renderChildren() {
        if (!this.props.route.length) {
            return;
        }
        const children = this.props.children;
        let slug = this.props.route[0],
            details = this.props.route[1];
        // если несколько страниц
        if (children && children.length) {
            let childrens = children.filter(child => {
                if (child.props.slug == slug) {
                    if (child.props.details && details) {
                        return child;
                    } else if (!child.props.details && !details) {
                        return child;
                    }
                }
            });
            if (childrens.length) {
                return childrens;
            } else {
                return children.find(child => child.props.slug == '*');
            }
        }
        // если одна страница
        else if (children && (children.props.slug == slug || children.props.slug == '*')) {
            if (children.props.details && details) {
                return children;
            } else if (!children.props.details && !details) {
                return children;
            }
        }
    }

    render() {
        return <main className={this.props.css}>
            {this._renderChildren()}
        </main>;
    }

}

export default Router;
