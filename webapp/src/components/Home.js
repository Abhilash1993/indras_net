import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";



class Home extends Component {
    api_server = 'https://indrasnet.pythonanywhere.com/';
    state = {
        msg: '',
        allItems: [],
        loadingData: false,
    }

    async componentDidMount() {
        try {
            this.setState({ loadingData: true });
            document.title = "Indra | Home";
            const res = await axios.get(this.api_server + 'models')
            this.setState({ allItems: res.data });
            this.setState({ loadingData: false });
            const doc = localStorage.getItem("doc");
            this.setState({doc:doc});
            console.log(this.state.allItems)
        } catch (e) {
            console.log(e.message);
        } 
    }

    openDescription = () => {
        const link = 'https://gcallah.github.io/indras_net/index.html'
        window.open(link)
    }

    renderShowDescription = () => {
        console.log("renderShowDescription called")
        return <h1 style={{"fontSize": 16, "fontWeight": '400'}}>
        <a href="#" className="text-primary m-2" onClick={this.openDescription}>
        View Project Description </a> </h1>
    }

    handleClick(id, name, source){
        localStorage.setItem("menu_id", id)
        localStorage.setItem("name", name)
        localStorage.setItem("source", source)
    }

    renderImage = () => {
        const sandpile_img = require('./images/Sandpile.jpg')
        var settings = {
              dots: true,
              infinite: true,
              speed: 500,
              slidesToShow: 1,
              slidesToScroll: 1,
              autoplay: true
            };
        //Please add the path of the images we wish to use in the carousel to the ListOfImages list.
        var ListOfImages = [sandpile_img,sandpile_img,sandpile_img]
        return <div>
            <Slider {...settings}>
                 {ListOfImages.map((pathOfImage,index) => {
                     return <div key ={index}>
                        <img src={pathOfImage}
                        className="rounded-circle"
                        alt="Responsive image"
                        style={{display:'block', width:'100%', alignItems: "center"}}
                        data-toggle="tooltip" data-placement="top" title="by Seth Terashima."/>
                    </div>
                })}
            </Slider>
        </div>
    }

    renderHeader = () => {
        return <h1 className={'text-center'}>Indra Agent-Based Modeling System</h1>
    }

    renderChooseModelProp = () => {
        return <h1 style={{"fontSize": 16, "fontWeight": '400'}}>Please choose a model: </h1>
    }

    render() {
        if (this.state.loadingData) {
            return (
            <Dimmer active inverted>
            <Loader size='massive'>Loading...</Loader>
            </Dimmer>
            );
        }
         const sandpile_img = require('./images/Sandpile.jpg')
        return (
            <div className={'container'}>
                <div>
                    {this.renderHeader()}
                </div>

                <br /><br />
                <br /><br />

                <div className={'row'}>
                    <div className={'col-6'}>
                        {this.renderChooseModelProp()}
                        <ul className="list-group">
                            <div className="row">
                                <div className="col">
                                    {Object.keys(this.state.allItems).map((item, i)=>
                                    <p className="w-50 p-3 list-group-item list-group-item-action"
                                        key={i}>
                                        {console.log(this.state.allItems[item]['model ID'])}
                                        <Link to={{pathname: `/models/props/${i}`}}
                                            className="text-primary" data-toggle="tooltip"
                                            data-placement="top" title={this.state.allItems[item]['doc']}
                                            onClick={() =>
                                                this.handleClick(this.state.allItems[item]['model ID'],
                                            this.state.allItems[item]['name'],
                                            this.state.allItems[item]['source'])}>
                                            {this.state.allItems[item]['name']}
                                        </Link>
                                    </p>)}
                                </div>
                            </div>
                        </ul>
                    </div>
                    <div className={'col-6'}>
                        {this.renderImage()}
                    </div>
                </div>
                {this.renderShowDescription()}
                <br /><br />
                <br /><br />
            </div>
        );
    }
}

export default Home;
