import React from 'react'

class Card extends React.Component {
    render() {
        return (
            <div className="flex items-center justify-center transform transition duration-300">
                <div className="w-full xl:w-1/2 3xl:w-1/3 py-4 px-8 bg-white shadow-lg rounded-lg my-10">
                    {this.props.children}
                </div>
            </div>
        );
    }
}

export default Card;