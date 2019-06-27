import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';
import { Link, Route } from 'react-router-dom';

class ModelDetail extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/props/';
  constructor(props) {
    super(props);
    this.state = {
      model_details: {},
      loadingData: false,
      disabled_button: false,
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.checkValidity = this.checkValidity.bind(this);
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Property";
    const {menu_id} = this.props.location.state;
    const properties = await axios.get(this.api_server + menu_id.id);
    this.setState({id:menu_id.id})
    this.setState({ model_details: properties.data });
    this.states(properties.data);
    this.errors(properties.data);
    this.setState({ loadingData: false });
  }
  
  states(data){
    //loop over objects in data and create object in this.state
    Object.keys(this.state.model_details).forEach(item => 
         this.setState({[item]: data[item]})
       );
  }
  errors(data){
    Object.keys(this.state.model_details).forEach(item => 
       this.setState(prevState => ({
          model_details: {
             ...prevState.model_details,          
             [item]: {                     
                  ...prevState.model_details[item],  
                  errorMessage: ''        
                     }
                          }
  })))
  }

  handleChange = (e) =>{ 
   let model_detail = this.state.model_details;
   const {name,value} = e.target
   let valid = this.checkValidity(name,value)
   if (valid === 1){
      model_detail[name]['val']= value
      model_detail[name]['errorMessage']=""
      this.setState({model_details:model_detail})
      this.setState({disabled_button:false})
     
   }else if(valid === -1){
      model_detail[name]['errorMessage']="**Wrong Input Type"
      model_detail[name]['val']= this.state[name]['val']
      this.setState({model_details:model_detail})
      console.log(this.state.model_details[name])
      this.setState({disabled_button:true})
  }else{
      model_detail[name]['errorMessage']=`**Please input a number between ${this.state[name]['lowval']} and ${this.state[name]['hival']}.`
      model_detail[name]['val']= this.state[name]['val']
      this.setState({model_details:model_detail})
      this.setState({disabled_button:true})
    }       
  }
  
  checkValidity(name,value){
    if (value<=this.state.model_details[name]['hival'] && value >=this.state.model_details[name]['lowval']){
       if (this.state.model_details[name]['atype'] === 'INT' && !!(value%1)=== false){
             return 1
      }else if(this.state.model_details[name]['atype'] === 'DBL'){
             return 1
      }else{
             return -1
      }
 }else{
             return 0
      }
 }
  handleSubmit = event => {
    event.preventDefault();
    axios.put(this.api_server + this.state.id,this.state.model_details)
      .then(res => {
        console.log(res);
        console.log(res.data);
      },
     console.log(this.state.model_details))
    this.props.history.replace( '/models/menu/' + this.state.id );
  }

  render() {
    const { disabled_button } = this.state;
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
            {
           Object.keys(this.state.model_details).map((item,i)=> {
                return(<label key={i}>{this.state.model_details[item]['question']} :<input type={this.state.model_details[item]['atype']} defaultValue={this.state.model_details[item]['val']} onChange={this.handleChange} name={item} /><span style={{color:"red",fontSize: 12}}>{this.state.model_details[item]['errorMessage']}</span><br/><br/></label>
            )})
        }
        </form>
        <br /><br />
        <button disabled={disabled_button} onClick={!disabled_button ? this.handleSubmit.bind( this ) : null}>Submit</button>
      </div>
    );
  }
}

export default ModelDetail;