import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';

class ModelDetail extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/props/';
  constructor(props) {
    super(props);
    this.state = {
      msg: '',
      model_detail: {},
      grid_height: {},
      grid_width: {},
      loadingData: false,
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Property";
    const {menu_id} = this.props.location.state
    const res = await axios.get(this.api_server + menu_id.id)
    this.setState({ model_detail: res.data });
    this.setState({grid_height: res.data['grid_height']});
    this.setState({grid_width: res.data['grid_width']})
    this.setState({ loadingData: false });
  }
  

  handleChange = (event) => {
   //this.setState({ [target['val']]: target.value });
   let newVar = JSON.parse(JSON.stringify(this.state[event.target.name]))
   //make changes to ingredients
    newVar['val'] = event.target.value 
    this.setState({
      [event.target.name] : newVar
    }) 
    console.log(this.state.grid_height);
    console.log(this.state.grid_height['val']);

    console.log(this.state.grid_width);
    console.log(this.state.grid_width['val']);
  }

  handleSubmit(event) {
    alert('grid_height: ' + this.state.grid_height);
    event.preventDefault();
  }

  render() {
    if (this.state.loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size='massive'>Loading...</Loader>
        </Dimmer>
      );
    }
    return (
      <div>
        <br />
        <br />
        <h1 style={{ "textAlign": "center" }}>Welcome to the Indra ABM platform!</h1>
        <h1 style={{ "textAlign": "left" }}> List of properties </h1>
        <br /><br />
        <form>
		      <label> {this.state.grid_height['question']} :</label>
			    <input type="int" defaultValue={this.state.grid_height['val']} name='grid_height' onChange={this.handleChange}/>
	        <br /><br/>
          <label> {this.state.grid_width['question']} :</label>
          <input type="int" defaultValue={this.state.grid_height['val']} name='grid_width' onChange={this.handleChange}/>
          <br /><br/>
        </form>
        <br /><br />
      </div>
    );
  }
}

export default ModelDetail;
