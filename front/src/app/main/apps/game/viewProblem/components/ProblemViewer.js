import Courses from "../ViewProblemPage";
import * as Actions from 'app/store/actions';
import { useDispatch, useSelector } from 'react-redux';
import Button from "@material-ui/core/Button";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import React, { useEffect, Component } from "react";
import { Document, Page, pdfjs } from "react-pdf";
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

//  const id = Courses.getId;
 console.log(Courses);


// function tmp(props) {

// const dispatch = useDispatch();
	
	
// const id = useSelector(({getProblemId}) => getProblemId.getId.count);
// const getId = function() {

//   dispatch(Actions.getProblemId())
//   console.log(id)
//   }

//    useEffect(() => {

//       getId();
  
//    });
//    return()=>{
//      id
//    }
// }

export default class Test extends Component {

  state = {
    numPages: null,
    pageNumber: 1
  };

  onDocumentLoadSuccess = document => {
    const { numPages } = document;
    this.setState({
      numPages,
      pageNumber: 1
    });
  };

  changePage = offset =>
    this.setState(prevState => ({
      pageNumber: prevState.pageNumber + offset
    }));

  previousPage = () => this.changePage(-1);

  nextPage = () => this.changePage(1);

  render() {
    const { numPages, pageNumber } = this.state;

    return (

      
      <React.Fragment>
        <div className="flex">
          <p>
            Page {pageNumber || (numPages ? 1 : "--")} of {numPages || "--"}
          </p>
          <ButtonGroup
            variant="contained"
            color="primary"
            aria-label="contained primary button group"
          >
            <Button disabled={pageNumber <= 1} onClick={this.previousPage}>
              PREVIOUS
            </Button>
            <Button disabled={pageNumber >= numPages} onClick={this.nextPage}>
              NEXT
            </Button>
          </ButtonGroup>
        </div>
        <Document
          file={`/assets/PDF/1.pdf`}
          onLoadSuccess={this.onDocumentLoadSuccess}
        >
          <Page pageNumber={pageNumber} />
        </Document>
      </React.Fragment>
    );
  }
}
